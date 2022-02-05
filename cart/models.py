from django.db import models
from shop.models import *
from django.contrib.auth.models import User
# from django.dispatch import receiver


# Cart_holder is "SQL" django model 
# is an object that hold the cart id, and point to cart items
class Cart (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="mycart")

    def __str__(self):
        return f"{self.user.username} "

# Cart_items is "SQL" django model
# is an object linked to product object, with qtt int
class Cart_Item (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart, related_name="items", blank=True, null=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name, self.quantity, self.cart} "

    def serialize(self):
        return{
            "productname" : self.product.name,
            "productunitprice" : self.product.price,
            "productquantity": self.quantity,
            "productimage": self.product.album.default().serialize()
        }


