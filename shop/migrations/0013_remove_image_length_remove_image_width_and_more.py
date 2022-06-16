# Generated by Django 4.0.4 on 2022-06-16 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_delete_variant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='length',
        ),
        migrations.RemoveField(
            model_name='image',
            name='width',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(blank=True, default=None, related_name='products', to='shop.categorie'),
        ),
    ]