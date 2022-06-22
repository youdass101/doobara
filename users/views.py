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
    if request.method == "POST":
        # is int
        # given order record id 
        orderid = request.POST['orderid']
        # is object 
        # order instance the first in list 
        order = Orders.objects.filter(id=orderid)[0]
        # is list of instance 
        # all order connected product item records 
        items = order.items.all()
        # is dict 
        # serilized copy of order record fields
        sorder = order.serialize()
        # is list of dict 
        # list of serialized copy of order item record objects list
        sitems = [item.serialize() for item in items]
        
    return render(request, "users/orderlog.html", {"order": sorder, "items": sitems})