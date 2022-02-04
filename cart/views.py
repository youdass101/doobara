from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


def cart(request):
    return render(request, "cart/cart.html")

def checkout(request):
    return render(request, "cart/checkout.html")


def shopaddtocart(request):
    if request.user.is_authenticated:
        print("at view")
        if request.method == "PUT":
            pid = json.loads(request.body)
            product = Product.objects.get(id=int(pid['pid']))
            user = request.user
            try:
                user.mycart
                try:
                    citem = Cart_Item.objects.get(product=product, cart=user.mycart)
                    citem.quantity += 1
                    citem.save()
                except:
                    Cart_Item.objects.create(product=product, quantity=1, cart=user.mycart)
            except:
                cart = Cart.objects.create(user=user)
                Cart_Item.objects.create(product=product, quantity=1, cart=user.mycart)
            
            return JsonResponse({"result":"done"}, status=201)
    else:
        return JsonResponse({"result":"login"}, status=201)


def cartcontext(request):
    return {'item': 4}