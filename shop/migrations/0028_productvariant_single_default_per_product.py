from django.db import migrations, models


def dedupe_default_variants(apps, schema_editor):
    ProductVariant = apps.get_model("shop", "ProductVariant")

    duplicate_product_ids = (
        ProductVariant.objects.filter(is_default=True)
        .values_list("product_id", flat=True)
    )

    seen = set()
    for product_id in duplicate_product_ids:
        if product_id in seen:
            continue
        seen.add(product_id)

        defaults_qs = ProductVariant.objects.filter(
            product_id=product_id,
            is_default=True,
        ).order_by("sort_order", "id")
        keep = defaults_qs.first()
        if not keep:
            continue
        defaults_qs.exclude(pk=keep.pk).update(is_default=False)


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0027_product_brand_product_sku_product_slug"),
    ]

    operations = [
        migrations.RunPython(
            dedupe_default_variants,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AddConstraint(
            model_name="productvariant",
            constraint=models.UniqueConstraint(
                condition=models.Q(is_default=True),
                fields=("product",),
                name="shop_one_default_variant_per_product",
            ),
        ),
    ]
