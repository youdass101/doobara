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
    if request.method == "POST":
        # is dict 
        # deliver information form from html request
        try: 
            # form = int(request.POST['current_address_id'])
            form =request.POST
            createorder(request, form, False) 

        except:
            form = Delivery_Information(request.POST)
            # create order

            createorder(request,form, True) 
        success = "Thank you for Your order"

        return render(request, "users/orderplace.html", {'ordermessage':success})