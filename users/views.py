from django.shortcuts import render
import objgraph

# Create your views here.
def register_login(request):
    objgraph.show_growth()

    return render(request, "users/register_login.html")


def myaccount(request):
    objgraph.show_growth()

    # if request.user.is_authenticated:
    return render(request, "users/account.html")
    # return render(request, "account/login.html")