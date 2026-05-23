from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0035_servicebadgeassignment'),
    ]

    operations = [
        migrations.CreateModel(
            name='NormalVariantFeatureAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.PositiveSmallIntegerField(default=0)),
                ('custom_title', models.CharField(blank=True, max_length=255)),
                ('custom_description', models.TextField(blank=True)),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='normal_variant_assignments', to='shop.productfeature')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feature_assignments', to='shop.normalproductvariant')),
            ],
            options={
                'ordering': ['sort_order', 'id'],
                'constraints': [models.UniqueConstraint(fields=('variant', 'feature'), name='shop_unique_normal_variant_feature_assignment')],
            },
        ),
        migrations.CreateModel(
            name='SystemVariantFeatureAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.PositiveSmallIntegerField(default=0)),
                ('custom_title', models.CharField(blank=True, max_length=255)),
                ('custom_description', models.TextField(blank=True)),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='system_variant_assignments', to='shop.productfeature')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feature_assignments', to='shop.productvariant')),
            ],
            options={
                'ordering': ['sort_order', 'id'],
                'constraints': [models.UniqueConstraint(fields=('variant', 'feature'), name='shop_unique_system_variant_feature_assignment')],
            },
        ),
    ]
