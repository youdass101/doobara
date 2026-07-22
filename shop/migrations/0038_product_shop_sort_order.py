from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0037_long_images"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="shop_sort_order",
            field=models.PositiveIntegerField(
                db_index=True,
                default=0,
                help_text="Lower numbers appear first in the default shop product order.",
            ),
        ),
    ]
