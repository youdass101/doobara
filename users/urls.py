from django.urls import path
from . import views

# allauth 
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns=[
    # Login and registration page 
    # path("register_login", views.register_login, name="register_login"),
    # all auth views
    path('accounts/', include('allauth.urls'), name="allauthlogin"),
    # My Account page
    path("myaccount", views.myaccount, name="myaccount"),
    path('logout', LogoutView.as_view()),
    path('placeorder', views.placeorder, name="placeorder"),
    path('order_log', view=views.order_log, name="order_log"),
    path('address_list', view=views.address_list, name="address_list"),
    path('new_edit_address', view=views.new_edit_address, name="new_edit_address"),
    path('update_address', view=views.update_address, name="update_address")

]