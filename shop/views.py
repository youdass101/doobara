from ctypes import util
from itertools import product
import re
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import *


def index(request):
    lop = Product.objects.filter(featured=True)
    slop = [row.serialize("main") for row in lop]
    return render(request, "shop/index.html", {"lop":slop[:5]})


def shop(request):
    lop = Product.objects.filter(active=True)
    slop = [row.serialize("main") for row in lop]
    return render(request, "shop/shop.html", {"lop":slop})


def filtering(request, locat):
    lop = Categorie.objects.get(name=locat).products.all()
    slop = [row.serialize("main") for row in lop]
    return render(request, "shop/shop.html", {"lop":slop})


def single_product(request, locat):
    product = Product.objects.get(name=locat).serialize("all")
    return render(request, "shop/single_product.html", {"product": product})


def contactus(request):
    return render(request, "shop/contactus.html")
  







