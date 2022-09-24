from django.db import models
from .modeling.images import *
from .modeling.serialize_helper import *
from django.dispatch import receiver

# Categories is (int(primary id) * string * string * int * int) model
# interp. Product categories database SQL table 
class Categorie(models.Model):
    # name is string
    # category name string max 255 characters
    name = models.CharField(max_length=255)
    # description is string
    # category description filed more than 1000 characters
    description = models.TextField()
    
    # instance -> string
    # what fileds to show on admin page
    def __str__(self):
        return f"{self.name} "

    # instance -> dict 
    # copy instance filterd data to a string dictionary
    def serialize(self):
        return {
            "name" : self.name,
            "description" : self.description
        }

# Product variant table
class VariantHolder(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


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
    created_time = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    # video is string(url arg)
    # product video URL string 
    video = models.URLField(blank=True)
    # album is model-object
    # one to one filed with album images tabel object 
    album = models.ForeignKey(ImageAlbum, related_name='model', on_delete=models.SET_NULL, null=True, blank=True) 
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
    category = models.ManyToManyField(Categorie, blank=True, default=None, related_name="products") 
    
    # IF any issue show will customize based on it so far when connected variant holder is deleted 
    #                       to connected product 
    # variantes are a list of objects
    # if product have a variant they will be listed
    variant_list = models.ForeignKey(VariantHolder, null=True, blank=True, default=None, related_name="products", on_delete=models.SET_NULL)
    # Variant_name is the string 
    # if variant true, name is the variant keyword of the product
    variant_name = models.CharField(max_length=255, blank=True, null=True, default=None)
    # Variant_default is a boolean 
    # if product is variant and is the default variant in list result is true 
    variant_default = models.BooleanField(default=False)

    # Admin page tabel view of dojects column (key value)
    def __str__(self):
        return f"{self.name}, {self.album} "

    # SQL query set -> Dictionary(json)
    # Takes SQL(model) query set data and convert it to JSON dictionary records
    #  Using helper file to breack down the model serializiation
    def serialize(self, tag):
        # function at helper file 
        return product_serialize(self, tag)

# !!! TEST IT IF ITS STILL WORKING AFTER THE VARIANT CUSTOMIZATION !!!
# Delete product foreing connected objects
@receiver(models.signals.post_delete, sender=Product)
def handle_deleted_product(sender, instance, **kwargs):
    # if instance.variant_list:
    #     instance.variant_list.delete()
    if instance.album:
        instance.album.delete()