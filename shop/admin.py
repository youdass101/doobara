from django.contrib import admin
from .models import *

from import_export.admin import ImportExportActionModelAdmin

class ProductAdmin(ImportExportActionModelAdmin):
    list_display = ("name", "slug", "brand", "sku", "price", "active", "featured")
    search_fields = ("name", "slug", "brand", "sku")
    prepopulated_fields = {"slug": ("name",)}


class ShopModelAdmin(ImportExportActionModelAdmin):
    pass

# Register your models here.
admin.site.register(Categorie, ShopModelAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ShopModelAdmin)
admin.site.register(ProductVariant, ShopModelAdmin)
admin.site.register(ProductVariantImage, ShopModelAdmin)
admin.site.register(ProductVariantItem, ShopModelAdmin)
admin.site.register(Hero_Card, ShopModelAdmin)
