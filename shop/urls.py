
from . import views
from django.urls import path


urlpatterns=[
    # Index page or Home page 
    path("", views.index, name="index"),
    # Shop page for all products 
    path("shop", views.shop, name="shop"),
    # Shop page filtering product subpage
    path("shop/<str:locat>/", views.filtering, name="filtering"),
    # Contact Us page 
    path("contactus", views.contactus, name="contactus"),
    # Single product page
    path('single_product/<str:locat>/', views.single_product, name="single_product"),
    # search keyword 
    path('search', views.search, name="search"),
    path("orderby", views.orderby, name="orderby")

 



]

