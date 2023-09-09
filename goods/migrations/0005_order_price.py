# Generated by Django 4.2.4 on 2023-09-09 16:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("goods", "0004_price_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="price",
            field=models.DecimalField(decimal_places=2, default=201, max_digits=8),
            preserve_default=False,
        ),
    ]
