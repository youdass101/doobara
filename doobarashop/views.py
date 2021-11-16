import re
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "doobarashop/index.html")


def shop(request):
    return render(request, "doobarashop/shop.html")

def blog(request):
    return render(request, "doobarashop/blog.html")

def video(request):
    return render(request, "doobarashop/video.html")

def contactus(request):
    return render(request, "doobarashop/contactus.html")

def myaccount(request):
    return render(request, "doobarashop/account.html")

def cart(request):
    return render(request, "doobarashop/cart.html")

def checkout(request):
    return render(request, "doobarashop/checkout.html")

def single_product(request):
    return render(request, "doobarashop/single_product.html")

def single_blog_post(request):
    return render(request, "doobarashop/single_blog_post.html")



