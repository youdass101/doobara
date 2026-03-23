from django.db import migrations, models


def dedupe_product_thumbnails(apps, schema_editor):
    ProductImage = apps.get_model("shop", "ProductImage")

    product_ids = (
        ProductImage.objects.filter(thumbnail=True)
        .values_list("product_id", flat=True)
        .distinct()
    )
    for product_id in product_ids:
        thumbs_qs = ProductImage.objects.filter(
            product_id=product_id,
            thumbnail=True,
        ).order_by("id")
        keep = thumbs_qs.first()
        if not keep:
            continue
        thumbs_qs.exclude(pk=keep.pk).update(thumbnail=False)


def dedupe_variant_thumbnails(apps, schema_editor):
    ProductVariantImage = apps.get_model("shop", "ProductVariantImage")

    variant_ids = (
        ProductVariantImage.objects.filter(thumbnail=True)
        .values_list("variant_id", flat=True)
        .distinct()
    )
    for variant_id in variant_ids:
        thumbs_qs = ProductVariantImage.objects.filter(
            variant_id=variant_id,
            thumbnail=True,
        ).order_by("id")
        keep = thumbs_qs.first()
        if not keep:
            continue
        thumbs_qs.exclude(pk=keep.pk).update(thumbnail=False)


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0028_productvariant_single_default_per_product"),
    ]

    operations = [
        migrations.RunPython(
            dedupe_product_thumbnails,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.RunPython(
            dedupe_variant_thumbnails,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AddConstraint(
            model_name="productimage",
            constraint=models.UniqueConstraint(
                condition=models.Q(thumbnail=True),
                fields=("product",),
                name="shop_one_product_thumbnail_per_product",
            ),
        ),
        migrations.AddConstraint(
            model_name="productvariantimage",
            constraint=models.UniqueConstraint(
                condition=models.Q(thumbnail=True),
                fields=("variant",),
                name="shop_one_variant_thumbnail_per_variant",
            ),
        ),
    ]
