from django.shortcuts import render
from .models import *
from django.http import  JsonResponse, HttpResponseRedirect
from django.urls import reverse
import json
from .modules.cartmanager import *
from users.forms import *
from .modules.snippethelper import *
from django.contrib.auth.decorators import login_required


# Request(model) -> render
# return the user or session cart data list 
def cart(request):
    cart = CartManager(request)
    return render(request, "cart/cart.html", {"cart": cart.cart_page()})


# WHen user press the add to cart button
# this view will add the given
def shopaddtocart(request):
    if request.method == "PUT":
        # load html input of product id
        cpid = json.loads(request.body)
        # is instance object
        # create new cart instance 
        cart = CartManager(request)
        # add time to cart using instance method
        cart.add_to_cart(cpid)
        # is dict
        # current cart data in dict
        ccart = cartcontext(request) 
        return JsonResponse({"result":"done", "cart": ccart}, status=201)

# dict (request) -> json dict
def updatecart(request):
    # is dict
    # json dict collect from js
    cartupdate = json.loads(request.body)
    # is instance 
    # create new cart instance
    dcart = CartManager(request)
    # use cart method to update cart data 
    dcart.update_cart(cartupdate)
 
    return JsonResponse({"result":"done"}, status=201)
    
@login_required
def checkout(request):
    # is instance object
    # create new cart instance 
    cart = CartManager(request)
    # is list 
    # all user address instances
    loa = request.user.myaddress.all()
    # is list of dict
    # create list of dict from objects
    lod = [item.serialize() for item in loa]
    # if method is GET
    if request.method == "GET":
        # is int 
        # get the address that has default as true
        id = default_address(lod)
    # is method is POST
    if request.method == "POST":
        # is int
        # given Id 
        id = int(request.POST['id'])

    # is dict 
    # create a list of data 
    output = {"form": Delivery_Information(),
            "cart":cart.cart_page(),
            "address_id":id, 
            "loa":lod}
    return render(request, "cart/checkout.html", output)
    # else:
    #     return HttpResponseRedirect(reverse('myaccount'))


# request -> dict
# DATA UPDATES COLLECTER return the user attached cart items qtty and total price 
def cartcontext(request):
    # is instance object
    # create new cart instance object 
    ccart = CartManager(request)
    # is dict * int
    items, total = ccart.cart_context_process()
    return {'item': items, 'total': "{:.2f}".format(total)}