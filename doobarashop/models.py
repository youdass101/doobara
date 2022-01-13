from django.db import models
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models.base import Model
from django.db.models.deletion import SET_NULL
from django.db.models.fields.related import ForeignKey
# from django.contrib.auth.models import AbstractBaseUser

# Categories is (int(primary id) * string * string * int * int) model
# interp. Product categories database SQL table 
class Categories(models.Model):
    # category name string max 255 characters
    name = models.CharField(max_length=255)
    # category description filed more than 1000 characters
    description = models.TextField()
    # self regerence for child category (CANCELED)
    # child_node = models.ForeignKey("self",null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='parent')
    # self reference for next category under same parent (CANCELED)
    # right_node = models.ForeignKey("self",null=True, blank=True, default=None, on_delete=models.SET_NULL, related_name='left')
    
    def __str__(self):
        return f"{self.name} "

# Create your models here.
# PRODUCT is (int (primary ID) * string * int * string * string * date * URL 
#             * boolean * boolean * boolean * boolean * boolean *  model reference) model
# interp.  product database SQL table 
class Product(models.Model):
    # product name string of max 255 char
    name = models.CharField(max_length=255)
    # product price decimal number 
    price = models.FloatField()
    # product short description more than 1000 char 
    short_description = models.TextField()
    #product long decription more than 1000 char
    long_description = models.TextField()
    # product creation date 
    created_time = models.DateTimeField()
    # product video URL string 
    video = models.URLField()
    # boolean true if product in stock, false if out of stock 
    stock = models.BooleanField(default=False)
    # boolean ture if the product is featured, else false
    featured = models.BooleanField(default=False)
    # if product have variant options true, else false
    variant = models.BooleanField(default=False)
    # true if product active, else false
    active = models.BooleanField(default=False)
    # true if product on discount, else if not false
    discount = models.BooleanField(default=False)
    # product category model reference many to many (the product can belong to several catergories)
    category = models.ManyToManyField(Categories, null=True, blank=True, default=None, related_name="products")
    
    def __str__(self):
        return f"{self.name} "






 

    