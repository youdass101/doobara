from django.urls import path
from . import views

# allauth 
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns=[
    path("", views.index, name="index"),
    path("shop", views.shop, name="shop"),
    path("blog", views.blog, name="blog"),
    path("video", views.video, name="video"),
    path("contactus", views.contactus, name="contactus"),
    path("myaccount", views.myaccount, name="myaccount"),
    path("cart", views.cart, name="cart"),
    path('single_product/<str:locat>/', views.single_product, name="single_product"),
    path("single_blog_post", views.single_blog_post, name="single_blog_post"),
    path("checkout", views.checkout, name="checkout"),
    path("register_login", views.register_login, name="register_login"),
    # all auth
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),



]

