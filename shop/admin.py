from django.contrib import admin
from django.utils.html import format_html
from django import forms
from import_export.admin import ImportExportActionModelAdmin

from .models import (
    Categorie,
    Hero_Card,
    Product,
    ProductImage,
    ProductVariant,
    ProductVariantImage,
    ProductVariantItem,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "image_preview", "alt_text", "thumbnail")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-height: 70px; border-radius: 4px;" />',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Preview"


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    fields = (
        "title",
        "tier",
        "price",
        "sale_price",
        "quantity",
        "active",
        "is_default",
        "sort_order",
    )
    show_change_link = True


class ProductVariantImageInline(admin.TabularInline):
    model = ProductVariantImage
    extra = 1
    fields = ("image", "image_preview", "alt_text", "thumbnail")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-height: 70px; border-radius: 4px;" />',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Preview"


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        help_texts = {
            "quantity": (
                "Inventory source of truth. Quantity > 0 = in stock. "
                "Quantity <= 0 = out of stock."
            ),
            "availability": (
                "Use Preorder only for products you intentionally sell before stock arrives. "
                "For normal inventory, availability is auto-aligned from quantity."
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get("quantity") or 0
        availability = cleaned_data.get("availability")

        # Keep preorder as an explicit operator choice.
        if availability != "preorder":
            cleaned_data["availability"] = "in stock" if quantity > 0 else "out of stock"

        return cleaned_data


@admin.register(Product)
class ProductAdmin(ImportExportActionModelAdmin):
    form = ProductAdminForm
    list_display = (
        "name",
        "slug",
        "brand",
        "sku",
        "price",
        "quantity",
        "active",
        "featured",
        "updated_time",
    )
    search_fields = ("name", "slug", "sku", "brand")
    list_filter = ("active", "featured", "availability", "stock", "category")
    ordering = ("-updated_time", "name")
    readonly_fields = ("stock", "created_time", "updated_time")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("category",)
    inlines = (ProductImageInline, ProductVariantInline)
    fieldsets = (
        (
            "Basic info",
            {
                "fields": (
                    "name",
                    "slug",
                    "brand",
                    "sku",
                    "active",
                    "featured",
                )
            },
        ),
        (
            "Pricing",
            {
                "fields": (
                    "price",
                    "sale_price",
                    "currency",
                )
            },
        ),
        (
            "Inventory",
            {
                "fields": (
                    "quantity",
                    "availability",
                    "variant",
                    "variant_name",
                    "variant_default",
                    "stock",
                )
            },
        ),
        (
            "Content",
            {
                "fields": (
                    "short_description",
                    "description",
                    "video",
                )
            },
        ),
        (
            "Shipping",
            {
                "fields": (
                    "weight",
                    "dimensions",
                )
            },
        ),
        (
            "Categories",
            {
                "fields": ("category",),
            },
        ),
        (
            "Advanced/internal",
            {
                "classes": ("collapse",),
                "fields": ("is_system",),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_time", "updated_time"),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        quantity = obj.quantity or 0
        obj.stock = quantity > 0
        super().save_model(request, obj, form, change)


@admin.register(ProductVariant)
class ProductVariantAdmin(ImportExportActionModelAdmin):
    list_display = (
        "title",
        "product",
        "tier",
        "price",
        "quantity",
        "active",
        "is_default",
        "sort_order",
    )
    search_fields = ("title", "product__name", "product__sku")
    list_filter = ("active", "tier", "currency", "is_default")
    ordering = ("product__name", "sort_order", "title")
    inlines = (ProductVariantImageInline,)
    fieldsets = (
        (
            "Variant",
            {
                "fields": (
                    "product",
                    "title",
                    "tier",
                    "active",
                    "is_default",
                    "sort_order",
                )
            },
        ),
        (
            "Pricing",
            {
                "fields": (
                    "price",
                    "sale_price",
                    "currency",
                )
            },
        ),
        (
            "Inventory",
            {
                "fields": (
                    "stock",
                    "quantity",
                )
            },
        ),
        (
            "Description",
            {
                "fields": ("short_description", "description"),
            },
        ),
    )


@admin.register(ProductImage)
class ProductImageAdmin(ImportExportActionModelAdmin):
    list_display = ("product", "alt_text", "thumbnail")
    search_fields = ("product__name", "product__sku", "alt_text")
    list_filter = ("thumbnail",)
    ordering = ("product__name", "id")


@admin.register(ProductVariantImage)
class ProductVariantImageAdmin(ImportExportActionModelAdmin):
    list_display = ("variant", "variant_product", "alt_text", "thumbnail")
    search_fields = ("variant__title", "variant__product__name", "alt_text")
    list_filter = ("thumbnail",)
    ordering = ("variant__product__name", "variant__title", "id")

    def variant_product(self, obj):
        return obj.variant.product

    variant_product.short_description = "Product"


@admin.register(Categorie)
class CategoryAdmin(ImportExportActionModelAdmin):
    list_display = ("name", "short_description")
    search_fields = ("name", "description")
    ordering = ("name",)

    def short_description(self, obj):
        if len(obj.description) <= 80:
            return obj.description
        return f"{obj.description[:77]}..."

    short_description.short_description = "Description"


@admin.register(ProductVariantItem)
class ProductVariantItemAdmin(ImportExportActionModelAdmin):
    list_display = ("variant", "included_product", "quantity")
    search_fields = ("variant__title", "variant__product__name", "included_product__name")
    list_filter = ("variant__product",)


@admin.register(Hero_Card)
class HeroCardAdmin(ImportExportActionModelAdmin):
    list_display = ("title", "tag", "price", "active")
    search_fields = ("title", "tag", "categorie")
    list_filter = ("active",)
