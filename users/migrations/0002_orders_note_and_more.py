# Generated by Django 4.0.4 on 2022-05-25 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='note',
            field=models.CharField(default='nothing', max_length=355),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='delivery_address_details',
            name='phone_number',
            field=models.CharField(max_length=8),
        ),
    ]
