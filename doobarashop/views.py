import re
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "doobarashop/index.html")


def shop(request):
    return render(request, "doobarashop/shop.html")


