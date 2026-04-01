from django.contrib import admin

from .models import Coupon, CouponUsage


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "active",
        "discount_type",
        "value",
        "minimum_subtotal",
        "usage_limit_total",
        "usage_limit_per_user",
        "valid_from",
        "valid_until",
        "applies_to_all",
    )
    list_filter = ("active", "discount_type", "applies_to_all")
    search_fields = ("code",)
    filter_horizontal = ("products", "categories")


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ("id", "coupon", "coupon_code_snapshot", "user", "order", "discount_amount", "created_at")
    search_fields = ("coupon_code_snapshot", "coupon__code", "user__username", "order__id")
    list_filter = ("coupon", "created_at")
    readonly_fields = ("coupon", "coupon_code_snapshot", "user", "order", "discount_amount", "created_at")
