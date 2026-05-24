from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0038_mediaasset_and_image_asset_links'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/images/'),
        ),
        migrations.AlterField(
            model_name='productvariantimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/variants/images/'),
        ),
    ]
