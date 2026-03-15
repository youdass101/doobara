from django.contrib import admin
from .models import *

from import_export.admin import ImportExportActionModelAdmin

class ProductAdmin(ImportExportActionModelAdmin):
    pass

# Register your models here.
admin.site.register(Categorie, ProductAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductAdmin)
admin.site.register(ProductVariant, ProductAdmin)
admin.site.register(ProductVariantImage, ProductAdmin)
admin.site.register(ProductVariantItem, ProductAdmin)
admin.site.register(Hero_Card, ProductAdmin)