from ..models import *
from ..forms import *
from cart.modules.cartmanager import *
from cart.modules.snippethelper import *
from django.db import transaction
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


def _build_order_item_snapshot(cart_item):
    # NEW: Build an immutable purchase snapshot from the exact cart selection
    # so historical orders do not fall back to mutable parent-product defaults.
    unit_price = cart_item.product.sale_price if cart_item.product.sale_price else cart_item.product.price
    product_name = cart_item.product.name

    # NEW: Preserve existing system-variant behavior by snapshotting the selected
    # system variant title and price at order-creation time.
    if cart_item.variant:
        unit_price = cart_item.variant.sale_price if cart_item.variant.sale_price else cart_item.variant.price
        product_name = cart_item.variant.title
    # NEW: For normal single-product variants, snapshot variant-specific price and
    # a display name that keeps parent product context for order/admin/email views.
    elif cart_item.normal_variant:
        unit_price = (
            cart_item.normal_variant.sale_price
            if cart_item.normal_variant.sale_price
            else cart_item.normal_variant.price
        )
        product_name = f"{cart_item.product.name} - {cart_item.normal_variant.title}"

    return {
        "product": cart_item.product,
        "quantity": cart_item.quantity,
        "price": unit_price,
        "product_name": product_name,
    }


def createorder(request, form, new):
    user = request.user
    # result = create_new_address(request, form)
    if new:
        if form.is_valid():
        # if result:
            # is intance 
            # create a new delivery address model object 
            state = False
            # is list
            # list of user saved delivery addresses
            allad = user.myaddress.all()
           
            if len(allad) == 0:
                state=True
            
            # record instance
            # create a new instance deliver address data
            note = form.cleaned_data.get('notes')
            form.instance.user = user
            form.instance.default = state
            delivery =form.save()        

        else:
            # return form as it is to reload it 
            return (False, form)
    else:
        # is instance object
        # current saved in data address
        id = int(form['current_address_id'])
        note = form.get('ordernote', '').strip()
        delivery = Delivery_Address_Details.objects.get(id=id)
        
    # Shipping method can come from checkout POST; persist selection first so totals stay deterministic.
    shipping_method_id = request.POST.get("shipping_method_id")
    if shipping_method_id:
        set_selected_shipping_method(request, int(shipping_method_id))

    # Centralized pricing calculation to keep cart/checkout/order totals consistent.
    pricing = cart_pricing_breakdown(request)
    total = "{:.2f}".format(pricing["total"])
    shipping_method = pricing["shipping_method"]
    shipping_label = shipping_method.label if shipping_method else ""
    shipping_price = pricing["shipping_price"]

    # Reliability + performance:
    # Create order and move items in one transaction so partial writes cannot happen.
    # Also use bulk_create for order items to minimize insert queries.
    with transaction.atomic():
        # is instance 
        # create an new order object model
        order = Orders.objects.create(
            user=user,
            address=delivery,
            total=total,
            note=note,
            shipping_method=shipping_method,
            shipping_label=shipping_label,
            shipping_price=shipping_price,
        )

        # NEW: Prefetch variant relations used by purchase snapshot selection logic.
        cart_items = list(user.mycart.items.select_related("product", "variant", "normal_variant"))
        # NEW: Convert each cart row into a variant-aware immutable purchase snapshot.
        item_snapshots = [_build_order_item_snapshot(item) for item in cart_items]
        Item_Order.objects.bulk_create(
            [
                Item_Order(
                    product=snapshot["product"],
                    quantity=snapshot["quantity"],
                    price=snapshot["price"],
                    product_name=snapshot["product_name"],
                    order=order,
                )
                for snapshot in item_snapshots
            ]
        )
        user.mycart.items.filter(id__in=[item.id for item in cart_items]).delete()
    
    return (True, order)

# dict -> dict * boolean
# takes request dict return: form data
# and boolean true if user have address saved or false if not
def address_post(form):
    # aleardy existing address (icluding any order note in form)
    if 'current_address_id' in form:
        # user have saved address
        state = False
    # new delivery address for logged in user (should include order note)
    else:
        # is dict                                              
        form = Delivery_Information(form)
        # is a helper function at modules, ordermanager 
        # new address 
        state = True 

    return form, state
            
def change_default_address(user, aid):
    # get current default addres and set it to default to false and and save model instance
    # loc: models
    old = Delivery_Address_Details.objects.get(user=user, default=True)
    old.default = False
    old.save()
    # set new address to default 
    # get new address and set default to true and save instance
    caddress = Delivery_Address_Details.objects.get(id=aid)
    caddress.default = True
    caddress.save()


def create_new_address(request, form):
    if form.is_valid():
        # add missing fields to form and save form to instance 
        form.instance.user = request.user
        form.instance.default = False
        form.save()
        return True
    else:
        return form


def send_order_confirmation_email_to_user_and_admin(order):
    # Compatibility fix:
    # checkout currently calls this function with order.serialize() (a dict),
    # while this function needs full model relations (user/address/items) for email rendering.
    if isinstance(order, dict):
        order_id = order.get("orderid") or order.get("id")
        if not order_id:
            return
        order = Orders.objects.select_related("user", "address").prefetch_related("items").filter(id=order_id).first()
        if not order:
            return

    customer_email = order.user.email
    if not customer_email:
        return

    customer_name = order.user.first_name or (order.address.name if order.address else "Customer")
    items = [
        {
            "product_name": item.product_name,
            "quantity": item.quantity,
            "price": item.price,
            "subtotal": item.price * item.quantity,
        }
        for item in order.items.all()
    ]

    # send email to user with order details
    subject = f"Order Confirmation - Order #{order.id}"
    from_email = "Doobara <info@doobara.com>"
    to = [customer_email]
    text_content = f"Thank you for your order #{order.id}, {customer_name}!"
    html_content = render_to_string("doobarashop/order_confirmation_email.html", {'user': order.user, 'order': order, 'items': items})
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    # send email to admin with order details
    subject = f"New Order Received - Order #{order.id}"
    to = ["info@doobara.com"]  # Replace with actual admin email
    text_content = f"A new order has been received: Order #{order.id}, {customer_name}"
    html_content = render_to_string("doobarashop/order_notification_admin.html", {'user': order.user, 'order': order, 'items': items})
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
