# Generated by Django 3.2.8 on 2022-02-03 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_product_created_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]