from django.shortcuts import render
from .models import *
from django.http import HttpResponse

# Create your views here.


def cart(request):
    return render(request, "doobarashop/cart.html")

def checkout(request):
    return render(request, "doobarashop/checkout.html")