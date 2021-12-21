from django.db import models
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models.base import Model
# from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

# PRODUCT is sql table
# interp.  product table 
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    stock = models.BooleanField()
    featured = models.BooleanField()
    