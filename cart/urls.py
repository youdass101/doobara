from django.urls import path
from . import views

# allauth 
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns=[
    # Cart page 
    path("cart", views.cart, name="cart"),
     # Chekout cart page 
    path("checkout", views.checkout, name="checkout"),
]