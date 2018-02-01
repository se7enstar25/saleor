# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-23 14:28
from __future__ import unicode_literals

from django.db import migrations, models


def fill_is_shipping_required(apps, schema_editor):
    OrderLine = apps.get_model('order', 'OrderLine')
    for line in OrderLine.objects.all():
        if line.product:
            line.is_shipping_required = (
                line.product.product_type.is_shipping_required)
            line.save(update_fields=['is_shipping_required'])


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0031_auto_20180119_0405'),
        ('product', '0048_product_class_to_type')
    ]

    operations = [
        migrations.AddField(
            model_name='orderline',
            name='is_shipping_required',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(fill_is_shipping_required, migrations.RunPython.noop)
    ]
