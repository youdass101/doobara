from operator import ipow
from django.shortcuts import redirect, render
from .models import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
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
                    "productid" : product.id,
                    "productunitprice" : cart[i]['price'],
                    "productquantity": cart[i]['quantity'],
                    "productimage": product.album.default().serialize()}, 
                    (int(cart[i]['quantity']) * float(cart[i]['price']))
                    ))
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

def updatecart(request):
    cartupdate = json.loads(request.body)
    if request.user.is_authenticated:
        user_cart = request.user.mycart
    else:
        cart = request.session['cart']
        request.session.set_expiry(10000)
        print("ALERT", request.session.get_expiry_date())
        for product in cartupdate['cart']:  
            cart[product['pid']]['quantity'] = product['quantity']
        request.session.save()
    
    return JsonResponse({"result":"done"}, status=201)



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