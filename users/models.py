from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from shop.models import *

# is model object
# user shippin address and information
class Delivery_Address_Details (models.Model):
    # is string
    # oreder Receiver name 
    name = models.CharField(max_length=255)
    # is string 
    # order receiver last name
    last_name = models.CharField(max_length=255)
    # is string
    # delivery city and town
    city_town = models.CharField(max_length=255)
    # is string 
    # delivery street name 
    street_name = models.CharField(max_length=255)
    # is string 
    # delivery building and appartment 
    building_appartment = models.CharField(max_length=255)
    # is number
    # reciever contact number 
    phone_number = models.CharField(max_length=8)
    # is string 
    # delivery additional details
    delivery_details = models.CharField(max_length=400, blank=True)
    # is object instance
    # user account 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="myaddress")
    # is boolean 
    # address default
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}, {self.city_town}, {self.id} "

# is object model 
# user orders 
class Orders (models.Model):
    # is instance 
    # user who placed the order 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="myorders")
    # is instance
    # delivery address of user who placed the order 
    address = models.ForeignKey(Delivery_Address_Details, on_delete=models.SET_NULL, null=True)
    # is string
    # status names 
    processing = "prcs"
    complete = "cmplt"
    canceled = "cncld"
    pending = "pndng"
    # is list 
    # list of status
    STATUS_CHOICES = [(processing, "processing"), (complete, "complete"), (canceled, "canceled"), (pending, "pending") ]
    # is string
    # order staus to pick from list of choices 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=processing)
    # is Decimal number 
    # order total cost
    total = models.DecimalField(max_digits=5, decimal_places=2)
    # is strin 
    # order notes 
    note = models.CharField(max_length=355,null=True, blank=True)

    def __str__(self):
        return f"{self.id} "



# is object model 
# single product items id, qtt and price for user specific order
class Item_Order (models.Model):
    # is instance 
    # product object
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    # is int
    # ordered product quantity 
    quantity = models.IntegerField()
    # is decimal 
    # product price when order is placed
    price = models.DecimalField(max_digits=5 ,decimal_places=2)
    # is string 
    # product name
    product_name = models.CharField(max_length=255)
    # is instance 
    # order number object 
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return f"{self.product_name} "


