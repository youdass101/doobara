from pyexpat import model
from django.db import models
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models.base import Model
from django.db.models.deletion import SET_NULL
from django.db.models.fields.related import ForeignKey
from .modeling.images import *
# from django.contrib.auth.models import AbstractBaseUser

# Categories is (int(primary id) * string * string * int * int) model
# interp. Product categories database SQL table 
class Categorie(models.Model):
    # name is string
    # category name string max 255 characters
    name = models.CharField(max_length=255)
    # description is string
    # category description filed more than 1000 characters
    description = models.TextField()
    
    def __str__(self):
        return f"{self.name} "

    def serialize(self):
        return {
            "name" : self.name,
            "description" : self.description
        }

class Variant(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name, self.title} "

    def serialize(self):
        return {
            "name" : self.name,
            "title" : self.title,
            "price" : self.price, 
            "default": self.default
        }

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
    album = models.OneToOneField(ImageAlbum, related_name='model', on_delete=models.CASCADE, null=True, blank=True) 
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
    category = models.ManyToManyField(Categorie, null=True, blank=True, default=None, related_name="products") 
    
    # variantes are a list of objects
    # if product have a variant they will be listed
    variant_list = models.ManyToManyField(Variant, null=True, blank=True, default=None, related_name="lov")

    # Admin page tabel view of dojects column (key value)
    def __str__(self):
        return f"{self.name}, {self.album} "

    # SQL query set -> Dictionary(json)
    # Takes SQL(model) query set data and convert it to JSON dictionary records
    def serialize(self, tag):
        # image is image object
        # if the object album is empty return none
        try:
            # if product have an album
            image = self.album.default()
        except:
            # else return None
            image = None

        # -> list of dictionary
        # convert a list of object to a list of dictionary usng helpers
        # if no obejcts exist return none to avoid erorrs
        def allimages():
            try:
                all = self.album.thumbnails()
                loi = [i.serialize() for i in all]
            except:
                loi = None
            return loi

        # is a Dictionary 
        if tag == 'main':
            return {
            "pname": self.name,
            "pprice": self.price,
            "pcategory": self.category.all(),
            "pmainimage": image.serialize(),
        }
        else:
            return {
                "pname": self.name,
                "pprice": self.price,
                "pshortdescription": self.short_description,
                "plongdescription": self.long_description,
                "pvideo": self.video,
                "pcreationdate": self.created_time,
                "pcategory": [cat.serialize() for cat in self.category.all()],
                "pmainimage": image.serialize(),
                "pallimages": allimages(),
                "pvariant" : [var.serialize() for var in self.variant_list.all()]
            }