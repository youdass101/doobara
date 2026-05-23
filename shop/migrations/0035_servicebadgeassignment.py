from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0034_alter_productfeature_icon_and_servicebadge_icon_to_filefield"),
    ]

    operations = [
        migrations.CreateModel(
            name="ServiceBadgeAssignment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
                ("custom_title", models.CharField(blank=True, max_length=255)),
                ("custom_description", models.TextField(blank=True)),
                (
                    "badge",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_assignments",
                        to="shop.servicebadge",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="service_badge_assignments",
                        to="shop.product",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order", "id"],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("product", "badge"),
                        name="shop_unique_product_service_badge_assignment",
                    )
                ],
            },
        ),
    ]
