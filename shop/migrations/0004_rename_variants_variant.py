# Generated by Django 3.2.8 on 2022-02-01 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_rename_categories_categorie'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Variants',
            new_name='Variant',
        ),
    ]