from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Delivery_Address_Details, Item_Order, Orders


class ItemOrderInline(admin.TabularInline):
    model = Item_Order
    extra = 0
    fields = ("product_name", "product", "price", "quantity")
    readonly_fields = ("product_name", "product", "price", "quantity")
    can_delete = False


@admin.register(Delivery_Address_Details)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "name",
        "last_name",
        "city_town",
        "phone_number",
        "default",
    )
    search_fields = (
        "user__username",
        "user__email",
        "name",
        "last_name",
        "phone_number",
        "city_town",
    )
    list_filter = ("default", "city_town")
    ordering = ("user__username", "id")


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "total",
        "status",
        "date",
        "shipping_label",
        "shipping_price",
        "coupon_code",
        "coupon_discount_amount",
    )
    list_filter = ("status", "date", "currency", "shipping_label")
    search_fields = (
        "id",
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
        "address__phone_number",
        "address__name",
        "address__last_name",
    )
    ordering = ("-date",)
    readonly_fields = ("id", "date")
    inlines = (ItemOrderInline,)
    fieldsets = (
        (
            "Order",
            {
                "fields": (
                    "id",
                    "status",
                    "date",
                )
            },
        ),
        (
            "Customer",
            {
                "fields": (
                    "user",
                    "address",
                )
            },
        ),
        (
            "Amounts",
            {
                "fields": (
                    "total",
                    "currency",
                    "shipping_method",
                    "shipping_label",
                    "shipping_price",
                    "coupon_code",
                    "coupon_discount_amount",
                )
            },
        ),
        (
            "Notes",
            {
                "fields": ("note",),
            },
        ),
    )


@admin.register(Item_Order)
class ItemOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product_name", "price", "quantity")
    search_fields = ("order__id", "product_name", "product__name")
    list_filter = ("order__status",)
    ordering = ("-order__date", "id")


class DoobaraUserAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_staff",
        "date_joined",
    )
    search_fields = ("username", "first_name", "last_name", "email")
    list_filter = ("is_active", "is_staff", "is_superuser", "date_joined")
    ordering = ("-date_joined",)


admin.site.unregister(User)
admin.site.register(User, DoobaraUserAdmin)
