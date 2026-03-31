from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from .models import *

class ProductAdmin(ImportExportActionModelAdmin):
    pass
# Register your models here.
admin.site.register(Video, ProductAdmin)
