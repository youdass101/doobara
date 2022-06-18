
from . import views
# allauth 
from django.urls import path


urlpatterns=[
    # Cart page 
    path("cart", views.cart, name="cart"),
     # Chekout cart page 
    path("checkout", views.checkout, name="checkout"),
    path("shopaddtocart", views.shopaddtocart, name="shopaddtocart"),
    path("updatecart", views.updatecart, name="updatecart")
]