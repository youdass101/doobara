from django.db import migrations, models
import django.db.models.deletion


def backfill_media_assets(apps, schema_editor):
    MediaAsset = apps.get_model('shop', 'MediaAsset')
    ProductImage = apps.get_model('shop', 'ProductImage')
    ProductVariantImage = apps.get_model('shop', 'ProductVariantImage')

    def asset_for_file(file_name, alt_text=''):
        if not file_name:
            return None
        asset, _ = MediaAsset.objects.get_or_create(
            file=file_name,
            defaults={
                'alt_text': alt_text or '',
                'title': '',
            },
        )
        if alt_text and not asset.alt_text:
            asset.alt_text = alt_text
            asset.save(update_fields=['alt_text'])
        return asset

    for image in ProductImage.objects.filter(image__isnull=False):
        if image.asset_id:
            continue
        asset = asset_for_file(image.image.name, image.alt_text)
        if asset:
            image.asset_id = asset.id
            image.save(update_fields=['asset'])

    for image in ProductVariantImage.objects.filter(image__isnull=False):
        if image.asset_id:
            continue
        asset = asset_for_file(image.image.name, image.alt_text)
        if asset:
            image.asset_id = asset.id
            image.save(update_fields=['asset'])


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0037_long_images'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaAsset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='product_media/')),
                ('alt_text', models.CharField(blank=True, max_length=255)),
                ('title', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='productimage',
            name='asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_images', to='shop.mediaasset'),
        ),
        migrations.AddField(
            model_name='productvariantimage',
            name='asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='variant_images', to='shop.mediaasset'),
        ),
        migrations.RunPython(backfill_media_assets, migrations.RunPython.noop),
    ]
