# from operator import ipow
# import re
from django.shortcuts import redirect, render
from requests import request
from .models import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
# from django.urls import reverse
import json
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.models import User
from .modules.helper import *

dcart = CartManager(request)

# Request(model) -> render
# return the user or session cart data list 
def cart(request):
    # print("this is",dcart)
    # print(dcart.cart)
    # if user is logged in
    if request.user.is_authenticated:
        # is dict
        # Get my cart model taht is connected to current use model 
        cart = request.user.mycart.items.all()
        # is list
        # json serialize list of dict objects
        scart = [(item.serialize(),(item.quantity * item.product.price)) for item in cart]
    # if user is not login use the session dict data 
    else: 
        # is dict
        # session cart dict  
        cart = request.session['cart']
        # is list of dict for each product in session cart dict
        scart = session_cart(cart)
    return render(request, "cart/cart.html", {"cart": scart})


def shopaddtocart(request):
    if request.method == "PUT":
        # load html input of product id
        cpid = json.loads(request.body)
        # load product object from Product model
        product = Product.objects.get(id=int(cpid['pid']))
        # if user is logged in
        if request.user.is_authenticated:
            # add product quantity to cart
            user_add_to_cart(request, cpid, product)
        # if user isn't logged in use session data 
        else:
            # add to session cart product qtt
            session_add_to_cart(request, cpid, product)
        # updated cart context after adding new data 
        cart = cartcontext(request) 
        return JsonResponse({"result":"done", "cart": cart}, status=201)

# dict (request) -> json dict
def updatecart(request):
    # is dict
    # json dict collect from js
    cartupdate = json.loads(request.body)
    # check is user is authenticated 
    update_cart(request, cartupdate)
    
    return JsonResponse({"result":"done"}, status=201)

def checkout(request):
    return render(request, "cart/checkout.html")

# request -> dict
# DATA UPDATES COLLECTER return the user attached cart items qtty and total price 
def cartcontext(request):
    # dict -> int * int
    # cart data process to get total items quatity and total price
    items, total = cart_context_process(request)
    return {'item': items, 'total': "{:.2f}".format(total)}