from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from .modules.ordermanager import *


# Create your views here.
# def register_login(request):
#     return render(request, "users/register_login.html")

 # if request.user.is_authenticated:
@login_required
def myaccount(request):
    return render(request, "users/account.html")

@login_required
def placeorder(request):
    form = Delivery_Information(request.POST)
    createorder(request,form) 

    return render(request, "users/orderplace.html")