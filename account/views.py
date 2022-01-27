from django.shortcuts import render

# Create your views here.
def register_login(request):
    return render(request, "accounts/register_login.html")


def myaccount(request):
    # if request.user.is_authenticated:
    return render(request, "accounts/account.html")
    # return render(request, "account/login.html")