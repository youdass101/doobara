
from unicodedata import name
from . import views
# allauth 
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns=[
    # Cart page 
    path("cart", views.cart, name="cart"),
     # Chekout cart page 
    path("checkout", views.checkout, name="checkout"),
    path("shopaddtocart", views.shopaddtocart, name="shopaddtocart"),
    path("updatecart", views.updatecart, name="updatecart")
]