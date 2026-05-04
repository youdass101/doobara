from django.db import migrations, models
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ("promotions", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coupon",
            name="code",
            field=models.CharField(max_length=50),
        ),
        migrations.AddConstraint(
            model_name="coupon",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("code"),
                name="promotions_coupon_code_ci_unique",
            ),
        ),
    ]
