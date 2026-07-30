from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0038_product_shop_sort_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="productimage",
            name="meta_image",
            field=models.BooleanField(
                default=False,
                help_text="Use this image as the main image in the Meta catalog feed.",
            ),
        ),
        migrations.AddConstraint(
            model_name="productimage",
            constraint=models.UniqueConstraint(
                condition=models.Q(("meta_image", True)),
                fields=("product",),
                name="shop_one_meta_image_per_product",
            ),
        ),
    ]
