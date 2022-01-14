from django.db import models
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models.base import Model
from django.db.models.deletion import SET_NULL
from django.db.models.fields.related import ForeignKey
# from .modeling.images import *
# from django.contrib.auth.models import AbstractBaseUser



# Categories is (int(primary id) * string * string * int * int) model
# interp. Product categories database SQL table 
class Categories(models.Model):
    # name is string
    # category name string max 255 characters
    name = models.CharField(max_length=255)
    # description is string
    # category description filed more than 1000 characters
    description = models.TextField()
    
    def __str__(self):
        return f"{self.name} "

# Create your models here.
# PRODUCT is model-table (int (primary ID) * string * int * string * string * date * URL
#                         * boolean * boolean * boolean * boolean * boolean *  model reference) model
# interp.  product database SQL table 
class Product(models.Model):
    # name is string
    # product name string of max 255 char
    name = models.CharField(max_length=255)

    # price is decimale number
    # product price decimal number 
    price = models.DecimalField(max_digits=5, decimal_places=2)

    # short_description is string 
    # product short description more than 1000 char 
    short_description = models.TextField(blank=True)

    # long_description is string
    #product long decription more than 1000 char
    long_description = models.TextField(blank=True)

    # created_time is date
    # product object creation date 
    created_time = models.DateTimeField()

    # video is string(url arg)
    # product video URL string 
    video = models.URLField(blank=True)

    # album is model-object
    # one to one filed with album images tabel object 
    # album = models.OneToOneField(ImageAlbum, related_name='model', on_delete=models.CASCADE, null=True, blank=True)
    
    # stock is boolean
    # boolean true if product in stock, false if out of stock 
    stock = models.BooleanField(default=False)

    # features is boolean
    # boolean ture if the product is featured, else false
    featured = models.BooleanField(default=False)

    # variant is boolean
    # if product have variant options true, else false
    variant = models.BooleanField(default=False)

    # active is boolean 
    # true if product active, else false
    active = models.BooleanField(default=False)

    # discount is boolean
    # true if product on discount, else if not false
    discount = models.BooleanField(default=False)

    # category is List of model-objects
    # product category model reference many to many (the product can belong to several catergories)
    category = models.ManyToManyField(Categories, null=True, blank=True, default=None, related_name="products")
    
    def __str__(self):
        return f"{self.name} "


    # SQL query set -> Dictionary(json)
    # Takes SQL(model) query set data and convert it to JSON dictionary records
    def serialize(self):
        return {
            "pname": self.name,
            "pprice": self.price,
            "pshortdescription": self.short_description,
            "plongdescription": self.long_description,
            "pvideo": self.video,
            "pcreationdate": self.created_time,
            "pcategory": self.category
        }



   







 

    