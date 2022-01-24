# Generated by Django 3.2.8 on 2022-01-14 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doobarashop', '0003_auto_20220113_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='long_description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='product',
            name='short_description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='video',
            field=models.URLField(blank=True),
        ),
    ]
