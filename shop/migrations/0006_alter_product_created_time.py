# Generated by Django 3.2.8 on 2022-02-03 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_variant_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]