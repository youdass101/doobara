from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0025_alter_productvariantimage_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="categorie",
            name="name",
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="product",
            name="active",
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name="product",
            name="featured",
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name="productvariant",
            name="active",
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AddIndex(
            model_name="productvariant",
            index=models.Index(
                fields=["product", "active", "sort_order"],
                name="shop_var_prod_act_sort_idx",
            ),
        ),
    ]
