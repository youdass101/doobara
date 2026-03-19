from django.db import models
from shop.models import *
from django.contrib.auth.models import User


# Dedicated delivery/shipping option model so options are fully data-driven.
# Admins can enable/disable, reorder, rename, or reprice methods without code changes.
class Shipping_Method(models.Model):
    label = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ("sort_order", "id")

    def __str__(self):
        return f"{self.label} (${self.price})"

# Cart_holder is "SQL" django model 
# is an object that hold the cart id, and point to cart items
class Cart (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="mycart")
    # Persist selected shipping method at cart level so cart and checkout stay in sync.
    shipping_method = models.ForeignKey(
        Shipping_Method,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="carts",
    )

    def __str__(self):
        return f"{self.user.username} "

# Cart_items is "SQL" django model
# is an object linked to product object, with qtt int
class Cart_Item (models.Model):
    # is object
    # objects list of connected Products
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    # is int
    # product quatity
    quantity = models.IntegerField()
    # is object
    # cart connected to the cart item
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.product.name, self.quantity, self.cart} "

    # object -> dict
    # convert object specified keys to a dict key/value
    def serialize(self):
        target_name = self.variant.title if self.variant else self.product.name
        target_price = self.variant.sale_price if self.variant and self.variant.sale_price else (self.variant.price if self.variant else self.product.price)
        if self.variant:
            image = self.variant.images.filter(thumbnail=True).first() or self.variant.images.first()
            cart_key = f"v-{self.variant.id}"
        else:
            image = self.product.images.filter(thumbnail=True).first() if self.product.images.filter(thumbnail=True).exists() else None
            cart_key = f"p-{self.product.id}"

        return{
            "productid" : self.product.id,
            "productname" : target_name,
            "productunitprice" : target_price,
            "productquantity": self.quantity,
            "productimage": image,
            "cartkey": cart_key,
        }
