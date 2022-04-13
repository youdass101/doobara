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
        # is dict
        # Get my cart model taht is connected to current use model 
        cart = request.user.mycart.items.all()
        # is list
        # json serialize list of dict objects
        scart = [(item.serialize(),(item.quantity * item.product.price)) for item in cart]
    else: 
        # is dict
        # session cart dict  
        cart = request.session['cart']
        # is list of dict for each product in session cart dict
        scart = session_cart(cart)
    return render(request, "cart/cart.html", {"cart": scart})

def checkout(request):
    return render(request, "cart/checkout.html")


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
    if request.user.is_authenticated:
        # is dict of objects
        user_cart = request.user.mycart
        # if delete value is true when x button is pressed in cart
        try: 
            # check value if true
            cartupdate['cart']['del']
            # is model object instance (class)
            product= Product.objects.get(id=cartupdate['cart']['pid'])
            # delete object
            Cart_Item.objects.get(product= product, cart=user_cart).delete()
        except:
            # loop over products in cart html
            for product in cartupdate['cart']:
                # is model instance 
                # single product object 
                po = Product.objects.get(id = int(product['pid']))
                # is model instance
                # Cart item in cart items related to use user 
                cit = Cart_Item.objects.get(product= po, cart=user_cart)
                # if new giver quatity is 0 delete product from cart item
                if (int(product['quantity']) == 0):
                    cit.delete()
                else:
                    # if new given qunatity is more than 0, adjust it
                    cit.quantity = int(product['quantity'])
                    cit.save()

    else:
        # is dict
        # the current session cart in request class 
        cart = request.session['cart']
        try:
            # delete the prouct from cart id the update given is for single product not list
            del cart[cartupdate['cart']['pid']]  
        except:
            # loop over list of product dict in cart html session
            for product in cartupdate['cart']:  
                # if new product quantity is 0 delete product from session cart
                if (int(product['quantity']) == 0 ):
                    del cart[product['pid']]
                else:
                    # if new given quantity is more than 0 change the current session 
                    # quantity to the given quantity
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