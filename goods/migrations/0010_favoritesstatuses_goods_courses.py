# Generated by Django 4.2.4 on 2023-09-21 10:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("goods", "0009_remove_order_price_id_order_price_alter_order_count_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="FavoritesStatuses",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "goods",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="goods.goods"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="goods",
            name="courses",
            field=models.ManyToManyField(
                through="goods.FavoritesStatuses", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
