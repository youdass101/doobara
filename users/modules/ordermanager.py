from ..models import *
from ..forms import *
from cart.modules.cartmanager import *
from cart.modules.snippethelper import *
from django.db import transaction
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from promotions.services import (
    check_usage_limits_atomic,
    record_coupon_usage,
    remove_coupon_from_session,
    snapshot_coupon_to_order,
)


def _build_checkout_error_form(message):
    # Centralize non-field checkout errors so caller can re-render checkout safely.
    # Call full_clean() first so cleaned_data exists before add_error() mutates form state.
    form = Delivery_Information(data={})
    form.full_clean()
    form.add_error(None, message)
    return form


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
    cart_items = list(user.mycart.items.select_related("product", "variant", "normal_variant"))
    if not cart_items:
        return (False, _build_checkout_error_form("Your cart is empty. Please add products before placing an order."))

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
        # Security: lock address selection to the authenticated user so posted
        # IDs cannot attach someone else's saved address to this order.
        try:
            delivery = Delivery_Address_Details.objects.get(id=id, user=user)
        except Delivery_Address_Details.DoesNotExist:
            return (False, _build_checkout_error_form("Selected delivery address is invalid. Please choose an address again."))
        
    # Shipping method can come from checkout POST; persist selection first so totals stay deterministic.
    shipping_method_id = request.POST.get("shipping_method_id")
    if shipping_method_id:
        set_selected_shipping_method(request, int(shipping_method_id))

    # Centralized pricing calculation to keep cart/checkout/order totals consistent.
    pricing = cart_pricing_breakdown(request)
    # Reuse the coupon validation already embedded in cart_pricing_breakdown()
    # so order totals and coupon snapshot/usage are based on one consistent read.
    coupon_pricing = {
        "coupon_code": pricing.get("coupon_code", ""),
        "coupon": pricing.get("coupon"),
        "coupon_valid": pricing.get("coupon_valid", False),
        "coupon_discount": pricing.get("coupon_discount", 0),
        "coupon_error": pricing.get("coupon_error", ""),
    }
    total = "{:.2f}".format(pricing["total"])
    shipping_method = pricing["shipping_method"]
    shipping_label = shipping_method.label if shipping_method else ""
    shipping_price = pricing["shipping_price"]

    # Reliability + performance:
    # Create order and move items in one transaction so partial writes cannot happen.
    # Also use bulk_create for order items to minimize insert queries.
    with transaction.atomic():
        if coupon_pricing["coupon_valid"]:
            # Re-check limits under row lock so concurrent checkouts cannot over-redeem capped coupons.
            usage_ok, usage_error, locked_coupon = check_usage_limits_atomic(coupon_pricing["coupon"], user)
            if not usage_ok:
                return (False, _build_checkout_error_form(usage_error))
            coupon_pricing["coupon"] = locked_coupon

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
            coupon_code=coupon_pricing["coupon_code"] if coupon_pricing["coupon_valid"] else "",
            coupon_discount_amount=coupon_pricing["coupon_discount"] if coupon_pricing["coupon_valid"] else 0,
        )

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
        if coupon_pricing["coupon_valid"]:
            # Snapshot and usage tracking happen only after a successful committed order.
            snapshot_coupon_to_order(order, coupon_pricing)
            record_coupon_usage(order, coupon_pricing)
            remove_coupon_from_session(request)
    
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
    # Clear current default only when it exists so first-time default assignment
    # cannot fail with DoesNotExist.
    old = Delivery_Address_Details.objects.filter(user=user, default=True).first()
    if old:
        old.default = False
        old.save(update_fields=["default"])
    # Security: only allow switching defaults within the same user's addresses.
    caddress = Delivery_Address_Details.objects.get(id=aid, user=user)
    caddress.default = True
    caddress.save(update_fields=["default"])


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
