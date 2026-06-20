# Generated manually to support guest checkout orders.

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0017_orders_coupon_code_orders_coupon_discount_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery_address_details',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='myaddress', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orders',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='myorders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orders',
            name='guest_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
