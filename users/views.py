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
    loo = Orders.objects.filter(user=request.user)
    orders = [order.serialize() for order in loo]
    return render(request, "users/account.html", {"orders": orders})

@login_required
def placeorder(request):
    if request.method == "POST":
        form, state = address_post(request)
        order = createorder(request,form, state) 
        success = "Thank you for Your order"

        return render(request, "users/orderplace.html", {'ordermessage':success, "order": order.serialize()})


@login_required
def order_log(request):
    return render(request, "users/orderlog.html")