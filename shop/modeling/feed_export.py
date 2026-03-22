from decimal import Decimal, InvalidOperation

from ..models import Product


def _primary_image(product):
    """
    Return the first preferred product image object (thumbnail first) or None.
    This stays internal so storefront serializers are not affected.
    """
    return product.images.filter(thumbnail=True).first() or product.images.first()


def _absolute_product_url(request, product):
    """
    Build an absolute canonical URL for feed export rows.
    """
    return request.build_absolute_uri(product.get_absolute_url())


def _absolute_image_url(request, product):
    """
    Build an absolute image URL when an image exists.
    Returns None for products with no images (null-safe requirement).
    """
    image = _primary_image(product)
    if not image:
        return None
    return request.build_absolute_uri(image.image.url)


def _normalized_availability(product):
    """
    Normalize availability values for catalog feeds.
    The rule intentionally mirrors existing inventory logic:
    - preorder flag takes priority
    - quantity > 0 => in stock
    - otherwise out of stock
    """
    inventory = product.get_inventory_data()
    if inventory["is_preorder"]:
        return "preorder"
    if inventory["in_stock"]:
        return "in stock"
    return "out of stock"


def _normalized_price(value):
    """
    Serialize Decimal/number values to a 2-decimal string used by feed payloads.
    Returns None for empty/invalid values so no fake values are emitted.
    """
    if value in (None, ""):
        return None
    try:
        return f"{Decimal(value):.2f}"
    except (InvalidOperation, TypeError, ValueError):
        return None


def product_feed_row(request, product):
    """
    Dedicated export row serializer for Merchant/Meta-ready catalog mapping.
    Kept separate from storefront serializers for backward compatibility.
    """
    description = (product.short_description or product.description or "").strip() or None

    row = {
        "id": str(product.id),
        "title": product.name,
        "description": description,
        "url": _absolute_product_url(request, product),
        "image_url": _absolute_image_url(request, product),
        "price": _normalized_price(product.sale_price or product.price),
        "currency": (product.currency or "").strip() or None,
        "availability": _normalized_availability(product),
        "brand": (product.brand or "").strip() or None,
        "sku": (product.sku or "").strip() or None,
        # Condition has no model source yet, so we expose a null and mark it as a gap.
        "condition": None,
    }

    row["missing_fields"] = [key for key, value in row.items() if value is None]
    return row


def product_feed_queryset():
    """
    Queryset used by feed export endpoint.
    Limited to active products to match publicly listed catalog behavior.
    """
    return Product.objects.filter(active=True).prefetch_related("images")


def build_product_feed_payload(request):
    """
    Build a JSON-safe payload for internal feed testing.
    """
    rows = [product_feed_row(request, product) for product in product_feed_queryset()]
    return {
        "fields": [
            "id",
            "title",
            "description",
            "url",
            "image_url",
            "price",
            "currency",
            "availability",
            "brand",
            "sku",
            "condition",
        ],
        "products": rows,
        "readiness_gaps": {
            "condition": "No source field exists on Product yet.",
            "gtin_mpn": "No GTIN/MPN fields exist yet (often required/recommended).",
            "google_product_category": "No mapped Google product category field exists yet.",
            "meta_fb_product_category": "No mapped Meta category field exists yet.",
        },
    }
