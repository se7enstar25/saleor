# Generated by Django 2.0.3 on 2018-08-22 12:20

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import django_measurement.models
import django_prices.models
import saleor.core.weight


def remove_legacy_shipping_methods(apps, schema_editor):
    ShippingMethod = apps.get_model("shipping", "ShippingMethod")
    ShippingMethod.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [("shipping", "0011_auto_20180802_1238")]

    operations = [
        migrations.RunPython(remove_legacy_shipping_methods, migrations.RunPython.noop)
    ]
