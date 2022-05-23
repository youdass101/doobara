from django.shortcuts import render
from .models import *
from django.http import  JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
import json
from .modules.cartmanager import *
from users.forms import *


# Request(model) -> render
# return the user or session cart data list 
def cart(request):
    cart = CartManager(request)
    return render(request, "cart/cart.html", {"cart": cart.cart_page()})


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
    print("json body data", cartupdate)
    dcart = CartManager(request)
    dcart.update_cart(cartupdate)
 
    
    return JsonResponse({"result":"done"}, status=201)
    
def checkout(request):
    if request.user.is_authenticated:
        # do something 
        return render(request, "cart/checkout.html", {"form": Delivery_Information()} )
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