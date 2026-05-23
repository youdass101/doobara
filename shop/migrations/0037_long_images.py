from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0036_variant_feature_assignments"),
    ]

    operations = [
        migrations.AddField(
            model_name="normalproductvariant",
            name="long_image",
            field=models.ImageField(blank=True, null=True, upload_to="products/normal_variants/long_images/"),
        ),
        migrations.AddField(
            model_name="productimage",
            name="long_image",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="productvariantimage",
            name="long_image",
            field=models.BooleanField(default=False),
        ),
    ]
