# Catalog Feed Readiness (Google Merchant + Meta Commerce)

This project now includes a **dedicated internal product feed export layer** that is intentionally separate from storefront serializers/templates.

## Internal endpoint

- `GET /internal/exports/products.json`

## Export fields (v2)

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
- `condition` (fixed value: `new`)
- `product_type` (internal category path)
- `google_product_category` (rule-based mapping where confident)
- `meta_fb_product_category` (rule-based mapping where confident)
- `missing_fields` (explicit per-row gap visibility)

## Availability normalization

Availability is normalized using existing inventory rules:

1. `preorder` when product inventory marks `is_preorder=True`
2. `in stock` when normalized quantity is greater than 0
3. `out of stock` otherwise

## Condition strategy

For the current catalog phase, all products are exported with:

- `condition = "new"`

## Product type strategy

`product_type` is generated from internal category names attached to each product.

- Category names are normalized and sorted
- Values are joined as a path using ` > `
- Example: `Security > Cameras`

## Category mapping strategy

The export uses an explicit rule table in `shop/modeling/feed_export.py`:

- Camera/PTZ/CCTV-like categories map to:
  - Google: `Electronics > Video > Video Cameras`
  - Meta: `Electronics > Cameras`
- Sensor-like categories map to:
  - Google: `Business & Industrial > Security & Surveillance > Sensors`
  - Meta: `Electronics > Smart Home Devices`
- Alarm/Siren-like categories map to:
  - Google: `Home & Garden > Household Supplies > Alarm Systems`
  - Meta: `Home Improvement > Home Security`

If no rule confidently matches, mapping fields remain `null` and the product is listed under manual mapping gaps.

## Readiness gaps (blocking full Merchant/Meta readiness)

The feed payload exposes global readiness gaps under `readiness_gaps`.
Current known gaps:

- `gtin_mpn` fields are missing
- products missing confident Google/Meta category mapping are listed in:
  - `manual_category_mapping_products`
  - `manual_category_mapping_product_types`
