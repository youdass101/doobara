from django.db import models
from .modeling.serialize_helper import *
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify

# Categories is (int(primary id) * string * string * int * int) model
# interp. Product categories database SQL table 
class Categorie(models.Model):
    # name is string
    # category name string max 255 characters
    # PERF (P2): indexed because category lookup by name is used in filter/navigation paths.
    name = models.CharField(max_length=255, db_index=True)
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


# PRODUCT is model-table (int (primary ID) * string * int * string * string * date * URL
#                         * boolean * boolean * boolean * boolean * boolean *  model reference) model
# interp.  product database SQL table 
class Product(models.Model):
    # name is string
    # product name string of max 255 char
    # PERF (P2): indexed because product lookups by name are used on product detail pages.
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    brand = models.CharField(max_length=255, blank=True)
    sku = models.CharField(max_length=64, blank=True)
    # long_description is string
    #product long decription more than 1000 char
    description = models.TextField(blank=True)
    # short_description is string 
    # product short description more than 1000 char 
    short_description = models.TextField(blank=True)
    # price is decimale number
    # product price decimal number 
    price = models.DecimalField(max_digits=5, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Sale price (if applicable)
    currency = models.CharField(max_length=3, default="USD")  # Currency code (e.g., USD, EUR)
    # category is List of model-objects
    # product category model reference many to many (the product can belong to several catergories)
    category = models.ManyToManyField(Categorie, blank=True, default=None, related_name="products") 

    # stock is boolean
    # boolean true if product in stock, false if out of stock 
    stock = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=0)  # Quantity available
    availability = models.CharField(
        max_length=50,
        choices=[
            ("in stock", "In Stock"),
            ("out of stock", "Out of Stock"),
            ("preorder", "Preorder"),
        ],
        default="in stock",
    )
    
    # created_time is date
    # product object creation date 
    created_time = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    # active is boolean 
    # true if product active, else false
    # PERF (P2): indexed since list pages frequently filter by active flag.
    active = models.BooleanField(default=False, db_index=True)
    # features is boolean
    # boolean ture if the product is featured, else false
    # PERF (P2): indexed because index page pulls featured products frequently.
    featured = models.BooleanField(default=False, db_index=True)
    updated_time = models.DateTimeField(auto_now=True)  # Product last updated date

    # video is string(url arg)
    # product video URL string 
    video = models.URLField(blank=True)


    # variant is boolean
    # if product have variant options true, else false
    variant = models.BooleanField(default=False)
    # Variant_name is the string 
    # if variant true, name is the variant keyword of the product
    variant_name = models.CharField(max_length=255, blank=True, null=True, default=None)
    # Variant_default is a boolean 
    # if product is variant and is the default variant in list result is true 
    variant_default = models.BooleanField(default=False)
    is_system = models.BooleanField(default=False)


    # Shipping and logistics
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Weight in kilograms
    dimensions = models.CharField(max_length=255, blank=True)  # Dimensions (e.g., "10x20x30 cm")
    

    def __str__(self):
        return f"{self.name}"
    
    def get_absolute_url(self):
        return reverse("single_product_by_slug", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "product"
            slug_candidate = base_slug
            counter = 2
            while Product.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                slug_candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug_candidate
        # Keep legacy inventory fields aligned to authoritative quantity rule.
        self.stock = self.in_stock
        self.availability = self.availability_label.lower()
        super().save(*args, **kwargs)

    @property
    def normalized_quantity(self):
        """
        Return a defensive integer quantity for stock checks.
        Keeps legacy/edge values safe (None, invalid types).
        """
        try:
            return int(self.quantity or 0)
        except (TypeError, ValueError):
            return 0

    @property
    def in_stock(self):
        """Authoritative availability rule: quantity > 0 means in stock."""
        return self.normalized_quantity > 0

    @property
    def availability_label(self):
        return "In Stock" if self.in_stock else "Out of Stock"

    def get_inventory_data(self):
        """
        Normalized inventory payload used by templates/serializers.
        Legacy fields are mirrored for backward compatibility.
        """
        in_stock = self.in_stock
        availability_label = self.availability_label
        normalized_quantity = self.normalized_quantity
        return {
            "in_stock": in_stock,
            "availability_label": availability_label,
            "quantity": normalized_quantity,
            # Backward-compatibility mirrors. Keep these until callers migrate.
            "stock": in_stock,
            "availability": availability_label.lower(),
        }

    # SQL query set -> Dictionary(json)
    # Takes SQL(model) query set data and convert it to JSON dictionary records
    #  Using helper file to breack down the model serializiation
    def serialize(self, tag):
        # function at helper file 
        return product_serialize(self, tag)

class Hero_Card(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    tag = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to= 'static/doobarashop/upload/images', blank=True, null=True)
    icon = models.CharField(max_length=1500, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    buton_text = models.CharField(max_length=255, blank=True)
    lifirst = models.CharField(max_length=255, blank=True)
    lesecond = models.CharField(max_length=255, blank=True)
    lethird = models.CharField(max_length=255, blank=True)
    lifirsti = models.CharField(max_length=1500, blank=True)
    lisecondi = models.CharField(max_length=1500, blank=True)
    lithirdi = models.CharField(max_length=1500, blank=True)
    classname = models.CharField(max_length=255, blank=True)
    link = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    categorie = models.CharField(max_length=255, blank=True)



    def __str__(self):
        return f"{self.title}"
    
    def serialize(self):
        return {
            "title": self.title,
            "description": self.description,
            "tag": self.tag,
            "image": self.image.url if self.image else None,
            "icon": self.icon,
            "price": int(self.price) if self.price else None,
            "buton_text": self.buton_text,
            "lifirst": self.lifirst,
            "lisecond": self.lesecond,
            "lethird": self.lethird,
            "lifirsti": self.lifirsti,
            "lisecondi": self.lisecondi,
            "lethirdi": self.lithirdi,
            "classname": self.classname,
            "link": self.link,
            "categorie": self.categorie
        }
    


# image is Sql django model
# interp each object contain image informations and url
class ProductImage(models.Model):
    # name is string
    # image title
    product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE)  # Link to the product
    # alt is string
    # image short interpretation 
    alt_text = models.CharField(max_length=255, blank=True)
    # image is image 
    # the image path
    image = models.ImageField(upload_to= 'static/doobarashop/upload/images')
    # default is boolean 
    # if true the image is the main image for the product 
    thumbnail = models.BooleanField(default=False)  # True if this is a thumbnail image


    # data to show on admin page 
    def __str__(self):
        return f"{self.product.name} - {self.alt_text}" 

class ProductVariant(models.Model):
    product = models.ForeignKey("Product", related_name="variants", on_delete=models.CASCADE)
    tier = models.CharField(max_length=20, choices=[("basic", "Basic"), ("advanced", "Advanced"), ("pro", "Pro")])
    title = models.CharField(max_length=255)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default="USD")
    stock = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True, db_index=True)
    is_default = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        indexes = [
            # PERF (P2): supports common detail-page variant query:
            # product filter + active filter + sort by sort_order.
            models.Index(fields=["product", "active", "sort_order"], name="shop_var_prod_act_sort_idx"),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.title}"

    @property
    def normalized_quantity(self):
        """
        Return a defensive integer quantity for stock checks.
        Keeps legacy/edge values safe (None, invalid types).
        """
        try:
            return int(self.quantity or 0)
        except (TypeError, ValueError):
            return 0

    @property
    def in_stock(self):
        """Authoritative availability rule: quantity > 0 means in stock."""
        return self.normalized_quantity > 0

    @property
    def availability_label(self):
        return "In Stock" if self.in_stock else "Out of Stock"

    def get_inventory_data(self):
        """
        Normalized inventory payload used by templates/serializers.
        Legacy fields are mirrored for backward compatibility.
        """
        in_stock = self.in_stock
        availability_label = self.availability_label
        normalized_quantity = self.normalized_quantity
        return {
            "in_stock": in_stock,
            "availability_label": availability_label,
            "quantity": normalized_quantity,
            # Backward-compatibility mirrors. Keep these until callers migrate.
            "stock": in_stock,
        }

    def save(self, *args, **kwargs):
        # Keep legacy inventory fields aligned to authoritative quantity rule.
        self.stock = self.in_stock
        super().save(*args, **kwargs)

class ProductVariantImage(models.Model):
    variant = models.ForeignKey("ProductVariant", related_name="images", on_delete=models.CASCADE)
    alt_text = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="static/doobarashop/upload/images")
    thumbnail = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.variant.product.name} - {self.variant.title} - {self.alt_text}"

class ProductVariantItem(models.Model):
    variant = models.ForeignKey("ProductVariant", related_name="package_items", on_delete=models.CASCADE)
    included_product = models.ForeignKey("Product", related_name="included_in_variants", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.variant.product.name} - {self.variant.title} includes {self.quantity} x {self.included_product.name}"

# !!! TEST IT IF ITS STILL WORKING AFTER THE VARIANT CUSTOMIZATION !!!
# Delete product foreing connected objects
# @receiver(models.signals.post_delete, sender=Product)
# def handle_deleted_product(sender, instance, **kwargs):
#     # if instance.variant_list:
#     #     instance.variant_list.delete()
#     if instance.album:
#         instance.album.delete()
