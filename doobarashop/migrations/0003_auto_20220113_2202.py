# Generated by Django 3.2.8 on 2022-01-13 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doobarashop', '0002_auto_20220113_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='variant',
            field=models.BooleanField(default=False),
        ),
    ]