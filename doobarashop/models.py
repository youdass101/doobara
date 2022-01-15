from django.db import models
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models.base import Model
from django.db.models.deletion import SET_NULL
from django.db.models.fields.related import ForeignKey
# from .modeling.images import *
# from django.contrib.auth.models import AbstractBaseUser

class ImageAlbum(models.Model):
    name = models.CharField(max_length=255)
    def default(self):
        return self.images.filter(default=True).first()
    
    def thumbnails(self):
        return self.images.filter(width=100, length=100)

    def __str__(self):
        return f"{self.name} " 

class Image(models.Model):
    # name is string
    # image title
    name = models.CharField(max_length=255)
    # alt is string
    # image short interpretation 
    alt = models.CharField(max_length=255, blank=True)
    # desctiption is string
    # image description 
    description = models.TextField(blank=True)
    # image is image 
    # the image path
    image = models.ImageField(upload_to= 'doobarashop/static/doobarashop/upload/images')
    # default is boolean 
    # if true the image is the main image for the product 
    default = models.BooleanField(default=False)
    # long is boolean 
    # if true it is for the product singal page long image 
    long = models.BooleanField(default=False)
    # album is model-object 
    # pointer to a specific album object id 
    album = models.ForeignKey(ImageAlbum, related_name='images', on_delete=models.CASCADE)

    width = models.FloatField(default=100)
    length = models.FloatField(default=100)

    def __str__(self):
        return f"{self.name}, {self.album} " 

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
    category = models.ManyToManyField(Categories, null=True, blank=True, default=None, related_name="products")
    
    # Admin page tabel view of dojects column (key value)
    def __str__(self):
        return f"{self.name}, {self.album} "

    # string(url) -> string(url)
    # take a url string removes the first prefix folder name
    def img_path_customize(self, ipath):
        return "/".join(ipath.strip("/").split('/')[1:])



    # SQL query set -> Dictionary(json)
    # Takes SQL(model) query set data and convert it to JSON dictionary records
    def serialize(self):
        # image is string(url)
        # the product main image url
        try:
            # if product have an album
            image = self.img_path_customize((self.album.default().image.url))
        except:
            # else return None
            image = None

        return {
            "pname": self.name,
            "pprice": self.price,
            "pshortdescription": self.short_description,
            "plongdescription": self.long_description,
            "pvideo": self.video,
            "pcreationdate": self.created_time,
            "pcategory": self.category,
        
            "pmainimage": image,
        }



   







 

    