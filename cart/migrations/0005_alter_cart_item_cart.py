# Generated by Django 3.2.8 on 2022-02-04 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_auto_20220204_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart_item',
            name='cart',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='items', to='cart.Cart'),
        ),
    ]