# Generated by Django 4.0.4 on 2022-05-19 21:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0012_delete_variant'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='delivery_address_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('city_town', models.CharField(max_length=255)),
                ('street_name', models.CharField(max_length=255)),
                ('building_appartment', models.CharField(max_length=255)),
                ('phone_number', models.IntegerField()),
                ('delivery_details', models.CharField(max_length=400)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myaddress', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('prcs', 'processing'), ('cmplt', 'complete'), ('cncld', 'canceled'), ('pndng', 'pending')], default='prcs', max_length=20)),
                ('total', models.DecimalField(decimal_places=2, max_digits=5)),
                ('address', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.delivery_address_details')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myorders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='item_order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('product_name', models.CharField(max_length=255)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='users.orders')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.product')),
            ],
        ),
    ]
