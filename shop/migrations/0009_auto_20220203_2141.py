# Generated by Django 3.2.8 on 2022-02-03 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_product_album'),
    ]

    operations = [
        migrations.CreateModel(
            name='VariantHolder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='variant_list',
        ),
        migrations.AddField(
            model_name='variant',
            name='variantholder',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='shop.variantholder'),
        ),
        migrations.AddField(
            model_name='product',
            name='variant_list',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='shop.variantholder'),
        ),
    ]
