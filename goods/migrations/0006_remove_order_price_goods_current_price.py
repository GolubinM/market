# Generated by Django 4.2.4 on 2023-09-09 17:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("goods", "0005_order_price"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="price",
        ),
        migrations.AddField(
            model_name="goods",
            name="current_price",
            field=models.DecimalField(decimal_places=2, default=1, max_digits=8),
            preserve_default=False,
        ),
    ]
