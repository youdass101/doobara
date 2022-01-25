from django.urls import path
from . import views

# allauth 
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns=[
    # Index page or Home page 
    path("", views.index, name="index"),
    # Shop page for all products 
    path("shop", views.shop, name="shop"),
    # Shop page filtering product subpage
    path("shop/<str:locat>/", views.filtering, name="filtering"),
    # Blog carousel page
    path("blog", views.blog, name="blog"),
    # Video Carousel page
    path("video", views.video, name="video"),
    # Contact Us page 
    path("contactus", views.contactus, name="contactus"),
    # My Account page
    path("myaccount", views.myaccount, name="myaccount"),
    # Single product page
    path('single_product/<str:locat>/', views.single_product, name="single_product"),
    # Single Blog Post page
    path("single_blog_post", views.single_blog_post, name="single_blog_post"),
    # Login and registration page 
    path("register_login", views.register_login, name="register_login"),
    # all auth views
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),



]

