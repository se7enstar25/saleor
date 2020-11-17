# Generated by Django 3.1 on 2020-09-16 11:23

import os

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.utils.text import slugify


def migrate_sale_data(apps, schema):
    Channel = apps.get_model("channel", "Channel")
    Sale = apps.get_model("discount", "Sale")
    SaleChannelListing = apps.get_model("discount", "SaleChannelListing")

    currency = os.environ.get("DEFAULT_CURRENCY", "USD")
    if Sale.objects.exists():
        channel, _ = Channel.objects.get_or_create(
            slug=slugify(settings.DEFAULT_CHANNEL_SLUG),
            defaults={"name": f"Channel {currency}", "currency": currency},
        )
        for sale in Sale.objects.iterator():
            SaleChannelListing.objects.create(
                sale=sale, channel=channel, discount_value=sale.value, currency=currency
            )


class Migration(migrations.Migration):

    dependencies = [
        ("channel", "0001_initial"),
        ("discount", "0021_auto_20200902_1249"),
    ]

    operations = [
        migrations.CreateModel(
            name="SaleChannelListing",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "discount_value",
                    models.DecimalField(decimal_places=3, default=0, max_digits=12),
                ),
                ("currency", models.CharField(max_length=3)),
                (
                    "channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sale_listings",
                        to="channel.channel",
                    ),
                ),
                (
                    "sale",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="channel_listings",
                        to="discount.sale",
                    ),
                ),
            ],
            options={"ordering": ("pk",), "unique_together": {("sale", "channel")}},
        ),
        migrations.RunPython(migrate_sale_data, migrations.RunPython.noop),
        migrations.RemoveField(model_name="sale", name="value",),
        migrations.AlterField(
            model_name="sale",
            name="type",
            field=models.CharField(
                choices=[("fixed", "fixed"), ("percentage", "%")],
                default="fixed",
                max_length=10,
            ),
        ),
    ]
