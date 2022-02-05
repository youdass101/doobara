from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


def cart(request):
    cart = request.user.mycart.items.all()
    scart = [(item.serialize(),(item.quantity * item.product.price)) for item in cart]
    return render(request, "cart/cart.html", {"cart": scart})

def checkout(request):
    return render(request, "cart/checkout.html")


def shopaddtocart(request):
    if request.user.is_authenticated:
        if request.method == "PUT":
            pid = json.loads(request.body)
            product = Product.objects.get(id=int(pid['pid']))
            user = request.user
            try:
                user.mycart
                try:
                    citem = Cart_Item.objects.get(product=product, cart=user.mycart)
                    citem.quantity += int(pid['quantity'])
                    citem.save()
                except:
                    print("do not exist")
                    Cart_Item.objects.create(product=product, quantity=pid['quantity'], cart=user.mycart)
            except:
                cart = Cart.objects.create(user=user)
                Cart_Item.objects.create(product=product, quantity=pid['quantity'], cart=user.mycart)
            
            cart = cartcontext(request)
            print(cart)
            return JsonResponse({"result":"done", "cart":cart}, status=201)
    else:
        return JsonResponse({"result":"login"}, status=201)

# request -> dict
# return the user attached cart items qtty and total price 
def cartcontext(request):
    if request.user.is_authenticated:
        cart = request.user.mycart.items.all()
        items = 0 
        total = 0
        for i in cart:
            items += i.quantity
            total += (i.quantity * i.product.price)

        return {'item': items, 'total': total}
    else:
        return {'item': 0, 'total': 0}