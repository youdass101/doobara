from django.shortcuts import render
from .models import *
from django.http import HttpResponse

# Create your views here.


def cart(request):
    return render(request, "cart/cart.html")

def checkout(request):
    return render(request, "cart/checkout.html")