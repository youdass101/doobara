from django.shortcuts import render
from .models import *
from django.http import  JsonResponse, HttpResponseRedirect
from django.urls import reverse
import json
from .modules.cartmanager import *
from users.forms import *


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
        cart = CartManager(request)
        cart.add_to_cart(cpid)
        cart = cartcontext(request) 
        return JsonResponse({"result":"done", "cart": cart}, status=201)

# dict (request) -> json dict
def updatecart(request):
    # is dict
    # json dict collect from js
    cartupdate = json.loads(request.body)
    dcart = CartManager(request)
    dcart.update_cart(cartupdate)
 
    return JsonResponse({"result":"done"}, status=201)
    

def checkout(request):
    if request.user.is_authenticated:
        cart = CartManager(request)
        loa = request.user.myaddress.all()
        lod = [item.serialize() for item in loa]
        id = 0
        if request.method == "GET":
            for i in lod:
                if i['default']:
                    id= int(i['id'])
        if request.method == "POST":
            id = int(request.POST['id'])
        return render(request, "cart/checkout.html", {"form": Delivery_Information(), "cart":cart.cart_page(), "address_id":id, "loa":lod})
    else:
        return HttpResponseRedirect(reverse('myaccount'))


# request -> dict
# DATA UPDATES COLLECTER return the user attached cart items qtty and total price 
def cartcontext(request):
    # dict -> int * int
    # cart data process to get total items quatity and total price
    ccart = CartManager(request)
    items, total = ccart.cart_context_process()
    return {'item': items, 'total': "{:.2f}".format(total)}