from django.db import models
from shop.models import *
from django.contrib.auth.models import User


# Cart_items is "SQL" django model
# is an object linked to product object, with qtt int
class Cart_Item (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

# Cart_holder is "SQL" django model 
# is an object that hold the cart id, and point to cart items
class Cart (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Cart_Item, related_name="cart", blank=True, null=True, default=None)




