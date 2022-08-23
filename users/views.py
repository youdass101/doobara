from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from .modules.ordermanager import *
import json
from .forms import *

# User account page render
# User has to be login
@login_required
def myaccount(request):
    # is list of instances
    # currnet user list of related records in orders model
    loo = Orders.objects.filter(user=request.user)
    # is list of dict 
    # copy list of serialized orders in loo list 
    orders = [order.serialize() for order in loo]
    try:
        # is instance
        # address instance with default set to true
        address = Delivery_Address_Details.objects.get(user=request.user, default=True)
        # is dict
        # default address serialized 
        saddress = address.serialize()
    except:
        saddress = False
    return render(request, "users/account.html", {"orders": orders, "address":saddress})

# Create a new order instance
@login_required
def placeorder(request):
    if request.method == "POST":
        # is mixed component
        # form is int or dict, state is boolean 
        # if state is true it means the address is new then form have the new data
        # if state is false then the form contain an id of current address 
        form, state = address_post(request)
        # is instance
        # new order instance
        order = createorder(request,form, state) 

        # If form has a valid data 
        if order[0]:
            # is string 
            # text to be shown on html page
            success = "Thank you for Your order"

            return render(request, "users/orderplace.html", {'ordermessage':success, "order": order[1].serialize()})
        # If new form have invalid data return same form and chekout page to retry
        else:
            return render(request, "cart/checkout.html", {"form": order[1], "cart": CartManager(request).cart_page()})

# render specific order instance and connected items
@login_required
def order_log(request):
    if request.method == "POST":
        # is int
        # given order record id 
        orderid = request.POST['orderid']
        # is object 
        # order instance the first in list 
        order = Orders.objects.filter(id=orderid)[0]
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

# render address list and change dedault address instance
def address_list(request):
    # if request.method == "GET":
    user = request.user
    loa = Delivery_Address_Details.objects.filter(user=user)
    sloa = [address.serialize() for address in loa]

    # Change user default  address 
    if request.method == "POST":
        result = json.loads(request.body)['id']
        # get current default addres and set it to default to false and and save model instance
        old = Delivery_Address_Details.objects.get(user=user, default=True)
        old.default = False
        old.save()
        # set new address to default 
        # get new address and set default to true and save instance
        caddress = Delivery_Address_Details.objects.get(id=result)
        caddress.default = True
        caddress.save()

    return render(request, "users/address_list.html",{"loa":sloa})

# render empty form for new address request or current address to edit in filled in form 
# Method get for new address and POST to existing address instance 
def new_edit_address(request):
    if request.method == "POST":
        # is dict 
        # html data post 
        data = request.POST
        # is instance
        # get deliver address using given ID
        address = Delivery_Address_Details.objects.get(user=request.user, id=data['edit-address'])
        # is form 
        # form filled with given address
        form = Delivery_Information(instance=address)
        # is int
        # delivery address id 
        info = data['edit-address']
        # is boolean 
        # false if address already exist and true if address is new
        type = False
    else:
        form = Delivery_Information()
        # is string
        # form address type one of 3 "new" "del" ""
        info = "new"
        # is boolean 
        # false if address already exist and true if address is new 
        type=  True

    return render(request, "users/new_edit_address.html", {"form": form, "new":type, "info": info})

# update existing address instance
def update_address(request):
    if request.method == "POST":
        # is string
        # one of 3 "new" * "del" * ""
        address_id = request.POST['info']
        # create new instance 
        if address_id == "new":
            # is form
            # fill form with given information
            new_address = Delivery_Information(request.POST)
            if new_address.is_valid:
                # add missing fields to form and save form to instance 
                new_address.instance.user = request.user
                new_address.instance.default = False
                new_address.save()
            
        # delete existing instance 
        elif address_id == "del":
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
            address = Delivery_Address_Details.objects.get(user=request.user, id = int(address_id))
            # is form
            # fill for with with existing address and edit fields using posted data form
            edit_address = Delivery_Information(request.POST, instance=address)
            # save instance updates
            edit_address.save()
            
        return redirect("/address_list")