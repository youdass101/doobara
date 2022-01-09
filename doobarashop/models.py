from django.db import models
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models.base import Model
from django.db.models.deletion import SET_NULL
from django.db.models.fields.related import ForeignKey
# from django.contrib.auth.models import AbstractBaseUser


class Categories(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    child_node = models.ForeignKey("self",null=True, blank=True, default=None, on_delete=models.SET_NULL)
    right_node = models.ForeignKey("self",null=True, blank=True, default=None, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"{self.name} "

# Create your models here.
# PRODUCT is sql table
# interp.  product table 
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    short_description = models.TextField()
    long_description = models.TextField()
    created_time = models.DateTimeField()
    video = models.URLField()
    stock = models.BooleanField()
    featured = models.BooleanField()
    variant = models.BooleanField()
    active = models.BooleanField()
    discount = models.BooleanField()
    category = models.ForeignKey(Categories, null=True, blank=True, default=None, on_delete=models.SET_NULL)
    def __str__(self):
        return f"{self.name} "






 

    