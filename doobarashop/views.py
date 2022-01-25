from ctypes import util
from itertools import product
import re
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import *



def index(request):
    lop = Product.objects.filter(featured=True)
    slop = [row.serialize() for row in lop]
    return render(request, "doobarashop/index.html", {"lop":slop})


def shop(request):
    lop = Product.objects.filter(active=True)
    slop = [row.serialize() for row in lop]
    return render(request, "doobarashop/shop.html", {"lop":slop})

def filtering(request, locat):
    lop = Categories.objects.get(name=locat).products.all()
    slop = [row.serialize() for row in lop]
    return render(request, "doobarashop/shop.html", {"lop":slop})


def blog(request):
    return render(request, "doobarashop/blog.html")

def video(request):
    return render(request, "doobarashop/video.html")

def contactus(request):
    return render(request, "doobarashop/contactus.html")

def myaccount(request):
    # if request.user.is_authenticated:
    return render(request, "doobarashop/account.html")
    # return render(request, "account/login.html")



def single_product(request, locat):
    product = Product.objects.get(name=locat)
    product = product.serialize()
    return render(request, "doobarashop/single_product.html", {"product": product})

def single_blog_post(request):
    return render(request, "doobarashop/single_blog_post.html")

def register_login(request):
    return render(request, "doobarashop/register_login.html")



