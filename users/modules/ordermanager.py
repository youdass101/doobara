from ..models import *
from ..forms import *
from cart.modules.cartmanager import *
from cart.modules.snippethelper import *
from django.db import transaction
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


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

        cart_items = list(user.mycart.items.select_related("product"))
        Item_Order.objects.bulk_create(
            [
                Item_Order(
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                    product_name=item.product.name,
                    order=order,
                )
                for item in cart_items
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
    # send email to user with order details
    if not order.email:
        return
    subject = f"Order Confirmation - Order #{order.id}"
    from_email = "Doobara <info@doobara.com>"
    to = [order.email]
    text_content = f"Thank you for your order #{order.id}, {order.user.first_name}!\n\n"
    html_content = render_to_string("doobarashop/order_confirmation_email.html", {'user': order.user, 'order': order})
    msg = EmailMultiAlternatives(subject, text_content, from_email, to) 
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    # send email to admin with order details
    subject = f"New Order Received - Order #{order.id}"
    from_email = "Doobara <info@doobara.com>"
    to = ["info@doobara.com"]  # Replace with actual admin email
    text_content = f"A new order has been received: Order #{order.id}, {order.user.first_name}, {order.address}\n\n"
    html_content = render_to_string("doobarashop/order_notification_admin.html", {'user': order.user, 'order': order})
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

