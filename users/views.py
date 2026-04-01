import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache

from cart.modules.snippethelper import cart_pricing_breakdown, get_active_shipping_methods
from cart.modules.cartmanager import CartManager
from promotions.services import pop_coupon_feedback

from .forms import Delivery_Information
from .models import Delivery_Address_Details, Orders
from .modules.ordermanager import (
    address_post,
    change_default_address,
    create_new_address,
    createorder,
    send_order_confirmation_email_to_user_and_admin,
)

# caller: main navigation
# User account page render
# User has to be login
@login_required
@never_cache
def myaccount(request):
    # is list of instances | (loc: models)
    # currnet user list of related records in orders model
    loo = Orders.objects.filter(user=request.user)
    # is list of dict 
    # copy list of serialized orders in loo list 
    orders = [order.serialize() for order in loo]
    try:
        # is instance | (loc: models)
        # address instance with default set to true
        address = Delivery_Address_Details.objects.get(user=request.user, default=True)
        # is dict
        # default address serialized 
        saddress = address.serialize()
    except Delivery_Address_Details.DoesNotExist:
        saddress = False
    return render(request, "users/account.html", {"orders": orders, "address":saddress})

# caller: checkout
# Create a new order instance
@login_required
@never_cache
def placeorder(request):
    if request.method != "POST":
        # placeorder is a write endpoint; redirect non-POST access to checkout.
        return redirect("checkout")

    if request.method == "POST":
        # is dictionarry form
        form =request.POST 
        # is mixed component | (loc: modules.ordermanager)
        # form is int or dict, state is boolean 
        # if state is true it means the address is new then form have the new data
        # if state is false then the form contain an id of current address 
        form, state = address_post(form)
        # is instance | (loc: modules.ordermanager)
        # new order instance
        order = createorder(request,form, state) 

        # If form has a valid data 
        if order[0]:
            # is string 
            # text to be shown on html page
            success = "Thank you for Your order"
            send_order_confirmation_email_to_user_and_admin(order[1].serialize())
            order_items = order[1].items.select_related("product").all()
            # GA4 analytics payload source for purchase event on thank-you page.
            analytics_items = []
            for item in order_items:
                category = ""
                if item.product:
                    first_category = item.product.category.first()
                    category = first_category.name if first_category else ""
                analytics_items.append(
                    {
                        "item_id": item.product.id if item.product else "",
                        "item_name": item.product_name,
                        "price": item.price,
                        "quantity": item.quantity,
                        "item_category": category,
                    }
                )

            return render(
                request,
                "users/orderplace.html",
                {
                    'ordermessage': success,
                    "order": order[1].serialize(),
                    "order_items": analytics_items,
                },
            )
        # If new form have invalid data return same form and chekout page to retry
        else:
            pricing = cart_pricing_breakdown(request)
            loa = request.user.myaddress.all()
            sloa = [item.serialize() for item in loa]
            return render(request, "cart/checkout.html", {
                "form": order[1],
                "cart": CartManager(request).cart_page(),
                "subtotal": pricing["subtotal"],
                "shipping_total": pricing["shipping_price"],
                "grand_total": pricing["total"],
                "coupon_code": pricing["coupon_code"],
                "coupon_discount": pricing["coupon_discount"],
                "coupon_valid": pricing["coupon_valid"],
                "coupon_error": pricing["coupon_error"],
                "coupon_feedback": pop_coupon_feedback(request),
                "selected_shipping_method": pricing["shipping_method"],
                "shipping_methods": get_active_shipping_methods(),
                "address_id": 0,
                "loa": sloa,
            })

# caller: account
# render specific order instance and connected items
@login_required
@never_cache
def order_log(request):
    if request.method != "POST":
        # Keep endpoint predictable: account page submits POST order IDs.
        return redirect("myaccount")

    # is int | HTML submited data 
    # given order record id 
    orderid = request.POST['orderid']
    # is object  | (loc: models)
    # order instance the first in list 
    # Security: ensure users can only access their own orders.
    order = get_object_or_404(Orders, id=orderid, user=request.user)
    # is list of instance 
    # all order connected product item records 
    items = order.items.all()
    # is dict 
    # serilized copy of order record fields
    sorder = order.serialize()
    # is list of dict 
    # list of serialized copy of order item record objects list
    sitems = [item.serialize() for item in items]

    return render(request, "users/orderlog.html", {"order": sorder, "items": sitems})


# caller: account 
# render address list and change dedault address instance
@login_required
@never_cache
def address_list(request):
    # if request.method == "GET":
    user = request.user 
    # is list of dict  | (loc: modules)
    loa = Delivery_Address_Details.objects.filter(user=user)
    sloa = [address.serialize() for address in loa]

    # Change user default  address 
    if request.method == "POST":
        # is string(number)
        # javascript submited data 
        aid = json.loads(request.body)['id']
        # get current default addres and set it to default to false and and save model instance
        # loc: modules.ordermanager
        change_default_address(user, aid)

    return render(request, "users/address_list.html",{"loa":sloa})


# caller: account
# render empty form for new address request or current address to edit in filled in form 
# Method get for new address and POST to existing address instance 
@login_required
@never_cache
def new_edit_address(request):
    if request.method == "POST":
        # is dict | HTML submited data 
        # html data post 
        data = request.POST
        # is instance | (loc: models)
        # get deliver address using given ID
        address = Delivery_Address_Details.objects.get(user=request.user, id=data['edit-address'])
        # is form 
        # form filled with given address
        form = Delivery_Information(instance=address)
        # is int | (loc: models)
        # delivery address id 
        info = data['edit-address']
        # is boolean 
        # false if address already exist and true if address is new
        type = False

    # Create new address
    else:
        # | (loc: forms)
        form = Delivery_Information()
        # is string
        # form address type one of 3 "new" "del" ""
        info = "new"
        # is boolean 
        # false if address already exist and true if address is new 
        type=  True

    return render(request, "users/new_edit_address.html", {"form": form, "new":type, "info": info})


@login_required
# caller: account 
# update existing address instance
@never_cache
def update_address(request):
    if request.method == "POST":
        # is string | HTML submited data
        # one of 3 "new" * "del" * ""
        address_state = request.POST['info']
        # create new instance 
        if address_state == "new":
            # is form | (loc: models)
            # fill form with given information
            new_address = Delivery_Information(request.POST)
            create_new_address(request, new_address)

        # delete existing instance 
        elif address_state == "del":
            # is int
            # D.A.D id
            id = request.POST['aid']
            # is instance
            # d.a.d instance using given ID 
            address = Delivery_Address_Details.objects.get(user=request.user, id = int(id))
            # delete selected instace 
            address.delete()

        # edit existing instance 
        else:
            # is instance 
            # get address instance using given id 
            address = Delivery_Address_Details.objects.get(user=request.user, id = int(address_state))
            # is form
            # fill for with with existing address and edit fields using posted data form
            edit_address = Delivery_Information(request.POST, instance=address)
            # save instance updates
            edit_address.save()
            
        return redirect("/address_list")
