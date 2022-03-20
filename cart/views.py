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
        # load html input of product id
        cpid = json.loads(request.body)
        # load product object
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

def updatecart(request):
    cartupdate = json.loads(request.body)
    if request.user.is_authenticated:
        user_cart = request.user.mycart
        try: 
            cartupdate['cart']['del']
            product= Product.objects.get(id=cartupdate['cart']['pid'])
            Cart_Item.objects.get(product= product, cart=user_cart).delete()
        except:
            for product in cartupdate['cart']:
                po = Product.objects.get(id = int(product['pid']))
                cit = Cart_Item.objects.get(product= po, cart=user_cart)
                if (int(product['quantity']) == 0):
                    cit.delete()
                else:
                    cit.quantity = int(product['quantity'])
                    cit.save()

    else:
        cart = request.session['cart']
        try:
            del cart[cartupdate['cart']['pid']]  
        except:
            for product in cartupdate['cart']:  
                if (int(product['quantity']) == 0 ):
                    del cart[product['pid']]
                else:
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