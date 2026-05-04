from django.conf import settings
from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone

from shop.models import Categorie, Product


class Coupon(models.Model):
    DISCOUNT_FIXED = "fixed"
    DISCOUNT_PERCENT = "percent"
    DISCOUNT_TYPE_CHOICES = (
        (DISCOUNT_FIXED, "Fixed amount"),
        (DISCOUNT_PERCENT, "Percent"),
    )

    code = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    usage_limit_total = models.PositiveIntegerField(null=True, blank=True)
    usage_limit_per_user = models.PositiveIntegerField(null=True, blank=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    applies_to_all = models.BooleanField(default=True)
    products = models.ManyToManyField(Product, blank=True, related_name="coupons")
    categories = models.ManyToManyField(Categorie, blank=True, related_name="coupons")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                Lower("code"),
                name="promotions_coupon_code_ci_unique",
            ),
        ]

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        # Store coupon codes in a canonical uppercase format so admin/data-import
        # writes stay aligned with case-insensitive lookup semantics.
        self.code = (self.code or "").strip().upper()
        return super().save(*args, **kwargs)

    def is_currently_valid_by_date(self, at_time=None):
        now = at_time or timezone.now()
        if self.valid_from and self.valid_from > now:
            return False
        if self.valid_until and self.valid_until < now:
            return False
        return True


class CouponUsage(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="usages")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.OneToOneField("users.Orders", on_delete=models.CASCADE, related_name="coupon_usage")
    coupon_code_snapshot = models.CharField(max_length=50)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.coupon_code_snapshot} / order {self.order_id}"
