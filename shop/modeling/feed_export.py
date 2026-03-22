from decimal import Decimal, InvalidOperation

from ..models import Product

# Explicit mapping table from internal category keywords to channel categories.
# Keep this list small and readable so business owners can maintain it safely.
#
# google_product_category values use official Google taxonomy-style paths.
# meta_fb_product_category values use readable Meta-facing category labels.
_CATEGORY_MAPPING_RULES = [
    {
        "keywords": {"camera", "ptz", "cctv"},
        "google_product_category": "Electronics > Video > Video Cameras",
        "meta_fb_product_category": "Electronics > Cameras",
    },
    {
        "keywords": {"sensor", "motion sensor"},
        "google_product_category": "Business & Industrial > Security & Surveillance > Sensors",
        "meta_fb_product_category": "Electronics > Smart Home Devices",
    },
    {
        "keywords": {"alarm", "siren"},
        "google_product_category": "Home & Garden > Household Supplies > Alarm Systems",
        "meta_fb_product_category": "Home Improvement > Home Security",
    },
]


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


def _category_names(product):
    """
    Return normalized internal category names attached to this product.
    """
    return [
        category.name.strip()
        for category in product.category.all()
        if (category.name or "").strip()
    ]


def _product_type_from_categories(product):
    """
    Build internal product_type from the store's own category path.
    Current model has flat categories, so we produce a stable joined path.
    """
    names = sorted(_category_names(product), key=str.lower)
    if not names:
        return None
    return " > ".join(names)


def _find_category_mapping(product):
    """
    Map internal categories to Google + Meta categories using keyword rules.
    Returns (google_category, meta_category) and leaves unknown cases unmapped.
    """
    haystack = " ".join(_category_names(product)).lower()
    if not haystack:
        return None, None

    for rule in _CATEGORY_MAPPING_RULES:
        if any(keyword in haystack for keyword in rule["keywords"]):
            return rule["google_product_category"], rule["meta_fb_product_category"]

    return None, None


def product_feed_row(request, product):
    """
    Dedicated export row serializer for Merchant/Meta-ready catalog mapping.
    Kept separate from storefront serializers for backward compatibility.
    """
    description = (product.short_description or product.description or "").strip() or None

    google_product_category, meta_fb_product_category = _find_category_mapping(product)

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
        # Business rule: all currently sold products are considered new condition.
        "condition": "new",
        "product_type": _product_type_from_categories(product),
        "google_product_category": google_product_category,
        "meta_fb_product_category": meta_fb_product_category,
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
    products_needing_manual_mapping = [
        {
            "id": row["id"],
            "title": row["title"],
            "product_type": row["product_type"],
            "missing_category_fields": [
                field
                for field in ("google_product_category", "meta_fb_product_category")
                if row.get(field) is None
            ],
        }
        for row in rows
        if row.get("google_product_category") is None or row.get("meta_fb_product_category") is None
    ]
    categories_needing_manual_mapping = sorted(
        {
            row["product_type"]
            for row in products_needing_manual_mapping
            if row.get("product_type")
        }
    )

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
            "product_type",
            "google_product_category",
            "meta_fb_product_category",
        ],
        "products": rows,
        "readiness_gaps": {
            "gtin_mpn": "No GTIN/MPN fields exist yet (often required/recommended).",
            "manual_category_mapping_products": products_needing_manual_mapping,
            "manual_category_mapping_product_types": categories_needing_manual_mapping,
        },
    }
