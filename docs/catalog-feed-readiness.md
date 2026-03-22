# Catalog Feed Readiness (Google Merchant + Meta Commerce)

This project now includes a **dedicated internal product feed export layer** that is intentionally separate from storefront serializers/templates.

## Internal endpoint

- `GET /internal/exports/products.json`

## Export fields (v1)

Each product row includes these keys:

- `id`
- `title`
- `description`
- `url` (canonical absolute product URL)
- `image_url` (absolute and null-safe)
- `price` (2-decimal string)
- `currency`
- `availability` (`in stock`, `out of stock`, `preorder`)
- `brand`
- `sku`
- `condition` (currently `null`; documented gap)
- `missing_fields` (explicit per-row gap visibility)

## Availability normalization

Availability is normalized using existing inventory rules:

1. `preorder` when product inventory marks `is_preorder=True`
2. `in stock` when normalized quantity is greater than 0
3. `out of stock` otherwise

## Readiness gaps (blocking full Merchant/Meta readiness)

The feed payload exposes global readiness gaps under `readiness_gaps`.
Current known gaps:

- `condition` source field is not stored on `Product`
- `gtin_mpn` fields are missing
- `google_product_category` mapping is missing
- `meta_fb_product_category` mapping is missing

These should be added in later iterations before direct API submissions.
