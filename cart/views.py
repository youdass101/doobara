from operator import ipow
from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .modules.helper import *


def cart(request):
    if request.user.is_authenticated:
        cart = request.user.mycart.items.all()
        scart = [(item.serialize(),(item.quantity * item.product.price)) for item in cart]
    else:
        scart = []
        cart = request.session['cart']
        for i in cart:
            product = Product.objects.get(id=i)
            scart.append(({"productname" : product.name,
                    "productunitprice" : cart[i]['price'],
                    "productquantity": cart[i]['quantity'],
                    "productimage": product.album.default().serialize()}, 
                    (int(cart[i]['quantity']) * float(cart[i]['price']))))
        print(scart)
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
            return JsonResponse({"result":"done", "cart": cart}, status=201)

# def updatecart(request):
#     cartupdate = json.loads(request.body)
#     if request.user.is_authenticated:


# request -> dict
# DATA UPDATES COLLECTER return the user attached cart items qtty and total price 
def cartcontext(request):
    items, total = 0, 0
    if request.user.is_authenticated:
        cart = request.user.mycart.items.all()
        for i in cart:
            items += i.quantity
            total += (i.quantity * i.product.price)
    else:      
        try:
            cart = request.session['cart']
            for i in cart:
                items += int(cart[i]['quantity'])
                total += (float(cart[i]['quantity']) * float(cart[i]['price']))
        except:
            request.session['cart'] = {}
            request.session.save()

    return {'item': items, 'total': "{:.2f}".format(total)}