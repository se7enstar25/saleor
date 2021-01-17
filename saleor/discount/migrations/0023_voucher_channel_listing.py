# Generated by Django 3.1 on 2020-09-21 08:26

import django.db.models.deletion
from django.db import migrations, models
from django.utils.text import slugify


def migrate_voucher_data(apps, schema_editor):
    Channel = apps.get_model("channel", "Channel")
    Voucher = apps.get_model("discount", "Voucher")
    VoucherChannelListing = apps.get_model("discount", "VoucherChannelListing")

    if Voucher.objects.exists():
        channels_dict = {}

        for voucher in Voucher.objects.iterator():
            currency = voucher.currency
            channel = channels_dict.get(currency)
            if not channel:
                name = f"Channel {currency}"
                channel, _ = Channel.objects.get_or_create(
                    currency_code=currency,
                    defaults={"name": name, "slug": slugify(name)},
                )
                channels_dict[currency] = channel
            VoucherChannelListing.objects.create(
                voucher=voucher,
                channel=channel,
                currency=currency,
                discount_value=voucher.discount_value,
                min_spent_amount=voucher.min_spent_amount,
            )


class Migration(migrations.Migration):

    dependencies = [
        ("discount", "0022_sale_channel_listing"),
    ]

    operations = [
        migrations.CreateModel(
            name="VoucherChannelListing",
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
                    models.DecimalField(decimal_places=3, max_digits=12),
                ),
                ("currency", models.CharField(max_length=3)),
                (
                    "min_spent_amount",
                    models.DecimalField(
                        blank=True, decimal_places=3, max_digits=12, null=True
                    ),
                ),
                (
                    "channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="voucher_listings",
                        to="channel.channel",
                    ),
                ),
                (
                    "voucher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="channel_listings",
                        to="discount.voucher",
                    ),
                ),
            ],
            options={"ordering": ("pk",), "unique_together": {("voucher", "channel")}},
        ),
        migrations.RunPython(migrate_voucher_data, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="voucher",
            name="currency",
        ),
        migrations.RemoveField(
            model_name="voucher",
            name="discount_value",
        ),
        migrations.RemoveField(
            model_name="voucher",
            name="min_spent_amount",
        ),
        migrations.AlterField(
            model_name="voucher",
            name="discount_value_type",
            field=models.CharField(
                choices=[("fixed", "fixed"), ("percentage", "%")],
                default="fixed",
                max_length=10,
            ),
        ),
    ]
