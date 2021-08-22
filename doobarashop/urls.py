from django.urls import path
from . import views

urlpatterns=[
    path("", views.index, name="index"),
    path("shop", views.shop, name="shop"),
    path("blog", views.blog, name="blog"),
    path("video", views.video, name="video"),
    path("contactus", views.contactus, name="contactus"),
    path("myaccount", views.myaccount, name="myaccount")

]

