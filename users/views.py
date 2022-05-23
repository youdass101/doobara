from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
# def register_login(request):
#     return render(request, "users/register_login.html")

 # if request.user.is_authenticated:
@login_required
def myaccount(request):
    return render(request, "users/account.html")