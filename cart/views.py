from operator import ipow
from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .modules.helper import *


def cart(request):
    cart = request.user.mycart.items.all()
    scart = [(item.serialize(),(item.quantity * item.product.price)) for item in cart]
    return render(request, "cart/cart.html", {"cart": scart})

def checkout(request):
    return render(request, "cart/checkout.html")


def shopaddtocart(request):
    if request.method == "PUT":
        # load product model object
        cpid = json.loads(request.body)
        product = Product.objects.get(id=int(cpid['pid']))
        if request.user.is_authenticated:
                user_add_to_cart(request, cpid, product)
                cart = cartcontext(request) 
                return JsonResponse({"result":"done", "cart":cart}, status=201)
        else:
            session_add_to_cart(request, cpid, product)
            cart = cartcontext(request) 
            return JsonResponse({"result":"login"}, status=201)

# request -> dict
# DATA UPDATES COLLECTER return the user attached cart items qtty and total price 
def cartcontext(request):
    items, total = 0, 0
    if request.user.is_authenticated:
        cart = request.user.mycart.items.all()
        for i in cart:
            items += i.quantity
            total += (i.quantity * i.product.price)

        return {'item': items, 'total': total}
    else:

        return {'item': 0, 'total': 0}