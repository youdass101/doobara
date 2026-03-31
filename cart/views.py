from django.shortcuts import render
from django.http import  JsonResponse
from django.contrib.auth.decorators import login_required
import json
# project files
from .models import *
from .modules.cartmanager import *
from users.forms import *
from .modules.snippethelper import *



# NOTES FOR OPTIMIZATION 
# Request the CartManager instance for the samse session is highly repetetive
# Other thant the CM repetation I cannot find any major optimazation that can be done 
# there is 38 line of codes and the rest commenting


# Request(model) -> render
# return the user or session cart data list 
def cart(request):
    # is list of dict | (loc: modules.cartmanager)
    # get user cart manager module list of dict for cart items related
    cm = CartManager(request).cart_page() # helper class in cartmanager
    pricing = cart_pricing_breakdown(request)
    shipping_methods = get_active_shipping_methods()
    return render(request, "cart/cart.html", {
        "cart": cm,
        "subtotal": pricing["subtotal"],
        "shipping_total": pricing["shipping_price"],
        "grand_total": pricing["total"],
        "selected_shipping_method": pricing["shipping_method"],
        "shipping_methods": shipping_methods,
    })

# caller: shop , index
# WHen user press the add to cart button
# this view will add the given
def shopaddtocart(request):
    if request.method == "PUT":
        # HTML submited data 
        # load html input of product id (cart product id)
        cpid = json.loads(request.body)
        # is instance object | (loc: modules.cartmanager)
        # create new cart manager instance 
        cm = CartManager(request)
        # add time to cart manager using instance method
        cm.add_to_cart(cpid)
        # is dict | (loc: modules.cartmanager)
        # current cart data in dict 
        ccart = cartcontext(request)
        return JsonResponse({"result":"done", "cart": ccart}, status=201)

# caller: cart
# dict (request) -> json dict
def updatecart(request):
    # is dict | Javascript submited data 
    # json dict collect from js page request contains product adjustment
    cartupdate = json.loads(request.body)
    # is instance | (loc: modules.cartmanager)
    # create new cart manager instance
    cm = CartManager(request) 
    # use cart method to update cart data items | (loc: modules.cartmanager)
    cm.update_cart(cartupdate)
    if "shipping_method_id" in cartupdate:
        set_selected_shipping_method(request, int(cartupdate["shipping_method_id"]))
 
    return JsonResponse({"result":"done"}, status=201)

# caller: cart     
@login_required
def checkout(request):
    # is instance object | (loc: modules.cartmanager)
    # create new cart manager instance 
    cm = CartManager(request)
    # is list | (loc: models)
    # all user address instances (list of address )
    loa = request.user.myaddress.all()
    # is list of dict
    # create list of dict from objects
    sloa = [item.serialize() for item in loa]
    # if method is GET
    # assign defualt address id to id variable
    if request.method == "GET":
        # is int 
        # get the address that has default as true
        aid = default_address(sloa)
    # is method is POST
    if request.method == "POST":
        # is int
        # given Id 
        aid = int(request.POST['id'])

    # is dict 
    # create a list of data wrapping all data in a dict 
    if request.method == "POST" and request.POST.get("shipping_method_id"):
        set_selected_shipping_method(request, int(request.POST["shipping_method_id"]))

    pricing = cart_pricing_breakdown(request)
    output = {"form": Delivery_Information(),
            "cart":cm.cart_page(),
            "address_id":aid, 
            "loa":sloa,
            "subtotal": pricing["subtotal"],
            "shipping_total": pricing["shipping_price"],
            "grand_total": pricing["total"],
            "selected_shipping_method": pricing["shipping_method"],
            "shipping_methods": get_active_shipping_methods(),}

    return render(request, "cart/checkout.html", output)


# request -> dict 
# DATA UPDATES COLLECTER return the user attached cart items qtty and total price 
def cartcontext(request):
    # | (loc: modules.cartmanager)
    # is dict * int (requested function from snippethelper file)
    items, total = cart_context_process(request)
    return {'item': items, 'total': "{:.2f}".format(total)}
