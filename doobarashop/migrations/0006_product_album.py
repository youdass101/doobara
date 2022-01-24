# Generated by Django 3.2.8 on 2022-01-14 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doobarashop', '0005_image_imagealbum'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='album',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='model', to='doobarashop.imagealbum'),
        ),
    ]
