from django.urls import path
from . import views

urlpatterns=[
    path("", views.index, name="index"),
    path("shop", views.shop, name="shop"),
    path("blog", views.blog, name="blog"),
    path("video", views.video, name="video"),
    path("contactus", views.contactus, name="contactus"),
    path("myaccount", views.myaccount, name="myaccount"),
    path("cart", views.cart, name="cart"),
    path("single_product", views.single_product, name="single_product"),
    path("single_blog_post", views.single_blog_post, name="single_blog_post"),
    path("checkout", views.checkout, name="checkout")
]

