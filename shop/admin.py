from django.contrib import admin
from .models import *

from import_export.admin import ImportExportActionModelAdmin

class ProductAdmin(ImportExportActionModelAdmin):
    pass

# Register your models here.
admin.site.register(Categorie, ProductAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Image, ProductAdmin)
admin.site.register(ImageAlbum, ProductAdmin)
admin.site.register(Variant, ProductAdmin)
admin.site.register(VariantHolder, ProductAdmin)