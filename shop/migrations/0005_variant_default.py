# Generated by Django 3.2.8 on 2022-02-01 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_rename_variants_variant'),
    ]

    operations = [
        migrations.AddField(
            model_name='variant',
            name='default',
            field=models.BooleanField(default=False),
        ),
    ]
