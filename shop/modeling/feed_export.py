import csv
import re
from decimal import Decimal, InvalidOperation

from django.http import HttpResponse
from django.urls import NoReverseMatch
from django.utils.html import strip_tags

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

# NEW: First-pass CSV columns requested for Google Merchant and Meta catalogs.
# Keep one shared ordered list so both endpoints stay consistent and easy to maintain.
_CSV_FIELDS = [
    "id",
    "title",
    "description",
    "availability",
    "condition",
    "price",
    "link",
    "image_link",
    "brand",
    "product_type",
    "additional_image_link",
]


def _primary_image(product):
    """
    Return the first preferred product image object (thumbnail first) or None.
    This stays internal so storefront serializers are not affected.
    """
    return product.images.filter(thumbnail=True).first() or product.images.first()


# NEW: System-tier variants have their own image relation, so we mirror existing
# "thumbnail first, then first image" behavior used across the project.
def _primary_system_variant_image(variant):
    return variant.images.filter(thumbnail=True).first() or variant.images.first()


def _absolute_product_url(request, product):
    """
    Build an absolute canonical URL for feed export rows.
    """
    try:
        return request.build_absolute_uri(product.get_absolute_url())
    except NoReverseMatch:
        # Legacy product records can predate slug enforcement. Use the older
        # detail URL as a safe fallback so one bad slug cannot break the feed.
        return request.build_absolute_uri(f"/single_product/{product.name}/")


def _absolute_file_url(request, file_field):
    """
    Build an absolute media URL without letting malformed legacy file values
    crash the entire catalog feed.
    """
    if not file_field:
        return None
    try:
        return request.build_absolute_uri(file_field.url)
    except (TypeError, ValueError):
        return None


def _absolute_image_url(request, product):
    """
    Build an absolute image URL when an image exists.
    Returns None for products with no images (null-safe requirement).
    """
    image = _primary_image(product)
    if not image:
        return None
    return _absolute_file_url(request, image.image)


# NEW: Build optional "additional_image_link" from non-primary product images.
# Merchant feeds accept a comma-separated list in a single column for CSV exports.
def _additional_product_image_urls(request, product):
    primary = _primary_image(product)
    urls = []
    for image in product.images.all():
        if primary and image.id == primary.id:
            continue
        image_url = _absolute_file_url(request, image.image)
        if image_url:
            urls.append(image_url)
    return ", ".join(urls) if urls else None


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


# NEW: Channel feeds require a clean plain-text description. We strip any HTML
# and collapse whitespace so both Google and Meta ingest stable text.
def _plain_text_description(value):
    text = strip_tags(value or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


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
    return Product.objects.filter(active=True).prefetch_related(
        "images",
        "category",
        "normal_variants",
        "variants__images",
    )


# NEW: Shared purchasable-offer expansion.
# We emit one row per actual selectable option when variants/tiers exist, and one
# row for simple products. This avoids ambiguous parent-level rows.
def _google_price(amount, currency):
    # Google Merchant requires the `price` field to include amount + ISO currency
    # in one value (e.g., "15.00 USD"). Returning None keeps invalid rows honest.
    normalized_amount = _normalized_price(amount)
    normalized_currency = (currency or "").strip().upper()
    if not normalized_amount or not normalized_currency:
        return None
    return f"{normalized_amount} {normalized_currency}"


def _base_product_offer_row(
    request,
    product,
    *,
    base_description,
    base_product_type,
    base_brand,
    base_link,
    base_condition,
    base_availability,
    google_price_format,
):
    """
    Build the parent product offer used for simple products and for active
    products whose variant/tier setup is not ready yet.
    """
    return {
        "id": str(product.id),
        "title": product.name,
        "description": base_description,
        "availability": base_availability,
        "condition": base_condition,
        "price": (
            _google_price(product.sale_price or product.price, product.currency)
            if google_price_format
            else _normalized_price(product.sale_price or product.price)
        ),
        "link": base_link,
        "image_link": _absolute_image_url(request, product),
        "brand": base_brand,
        "product_type": base_product_type,
        "additional_image_link": _additional_product_image_urls(request, product),
    }


def _iter_feed_offers(request, *, google_price_format=False):
    for product in product_feed_queryset():
        base_description = _plain_text_description(
            product.short_description or product.description
        )
        base_product_type = _product_type_from_categories(product)
        base_brand = (product.brand or "").strip() or None
        base_link = _absolute_product_url(request, product)
        base_condition = "new"
        base_availability = _normalized_availability(product)

        # System products: one row for each active tier/variant.
        if product.is_system:
            active_system_variants = product.variants.filter(active=True).order_by("sort_order", "id")
            if not active_system_variants:
                # Do not silently drop a newly active system product while its
                # tiers are still being configured in admin.
                yield _base_product_offer_row(
                    request,
                    product,
                    base_description=base_description,
                    base_product_type=base_product_type,
                    base_brand=base_brand,
                    base_link=base_link,
                    base_condition=base_condition,
                    base_availability=base_availability,
                    google_price_format=google_price_format,
                )
                continue

            for variant in active_system_variants:
                inventory = variant.get_inventory_data()
                variant_image = _primary_system_variant_image(variant)
                image_url = (
                    _absolute_file_url(request, variant_image.image)
                    if variant_image
                    else _absolute_image_url(request, product)
                )
                offer_description = _plain_text_description(
                    variant.short_description or variant.description or base_description
                )
                yield {
                    "id": f"{product.id}-system-{variant.id}",
                    "title": f"{product.name} - {variant.title}",
                    "description": offer_description,
                    "availability": "in stock" if inventory["in_stock"] else "out of stock",
                    "condition": base_condition,
                    "price": (
                        _google_price(variant.sale_price or variant.price, variant.currency)
                        if google_price_format
                        else _normalized_price(variant.sale_price or variant.price)
                    ),
                    "link": base_link,
                    "image_link": image_url,
                    "brand": base_brand,
                    "product_type": base_product_type,
                    "additional_image_link": _additional_product_image_urls(request, product),
                }
            continue

        # Non-system products with selectable normal variants: one row per variant.
        active_normal_variants = [
            variant for variant in product.normal_variants.all() if variant.active
        ]
        if active_normal_variants:
            for variant in sorted(active_normal_variants, key=lambda item: (item.sort_order, item.id)):
                image_url = (
                    _absolute_file_url(request, variant.image)
                    if variant.image
                    else _absolute_image_url(request, product)
                )
                offer_description = _plain_text_description(
                    variant.short_description or base_description
                )
                yield {
                    "id": f"{product.id}-variant-{variant.id}",
                    "title": f"{product.name} - {variant.title}",
                    "description": offer_description,
                    "availability": base_availability,
                    "condition": base_condition,
                    "price": (
                        _google_price(
                            variant.sale_price or variant.price,
                            getattr(variant, "currency", None) or product.currency,
                        )
                        if google_price_format
                        else _normalized_price(variant.sale_price or variant.price)
                    ),
                    "link": base_link,
                    "image_link": image_url,
                    "brand": base_brand,
                    "product_type": base_product_type,
                    "additional_image_link": _additional_product_image_urls(request, product),
                }
            continue

        # Simple products: one row using existing product-level purchasable fields.
        yield _base_product_offer_row(
            request,
            product,
            base_description=base_description,
            base_product_type=base_product_type,
            base_brand=base_brand,
            base_link=base_link,
            base_condition=base_condition,
            base_availability=base_availability,
            google_price_format=google_price_format,
        )


# NEW: Shared CSV response builder for scheduled catalog fetches.
def build_catalog_csv_response(request, *, filename, google_price_format=False):
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'inline; filename="{filename}"'

    writer = csv.DictWriter(response, fieldnames=_CSV_FIELDS, extrasaction="ignore")
    writer.writeheader()
    for row in _iter_feed_offers(request, google_price_format=google_price_format):
        writer.writerow(row)

    return response


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
