from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Delivery_Address_Details)
@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total', 'date')  # Add 'date' here
    list_filter = ('status', 'date')  # Optional: Add filters for status and date
    search_fields = ('user__username', 'status')  # Optional: Add search functionality
admin.site.register(Item_Order)
