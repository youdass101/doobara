from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from .modules.ordermanager import *
import json
from .forms import *

# caller: main navigation
# User account page render
# User has to be login
@login_required
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
    except:
        saddress = False
    return render(request, "users/account.html", {"orders": orders, "address":saddress})

# caller: checkout
# Create a new order instance
@login_required
def placeorder(request):
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

            return render(request, "users/orderplace.html", {'ordermessage':success, "order": order[1].serialize()})
        # If new form have invalid data return same form and chekout page to retry
        else:
            return render(request, "cart/checkout.html", {"form": order[1], "cart": CartManager(request).cart_page()})

# caller: account
# render specific order instance and connected items
@login_required
def order_log(request):
    if request.method == "POST":
        # is int | HTML submited data 
        # given order record id 
        orderid = request.POST['orderid']
        # is object  | (loc: models)
        # order instance the first in list 
        order = Orders.objects.get(id=orderid)
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


# caller: account 
# update existing address instance
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
            # if new_address.is_valid:
            #     # add missing fields to form and save form to instance 
            #     new_address.instance.user = request.user
            #     new_address.instance.default = False
            #     new_address.save()
            
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