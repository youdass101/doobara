from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *


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
    if form.is_valid():
        name = form.cleaned_data['first_name']
        lastname = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        city = form.cleaned_data['city_town']
        street = form.cleaned_data['street']
        building = form.cleaned_data['building_appartement']
        information = form.cleaned_data['additional_information']
        note = form.cleaned_data['note']

        delivery = delivery_address_details.objects.create(name=name, last_name=lastname, city_town=city, street_name=street, building_appartment=building, phone_number=phone, delivery_details=information, user=request.user)

    return render(request, "users/orderplace.html")