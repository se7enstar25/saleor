# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-16 11:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def assign_category_to_products(apps, schema_editor):
    Product = apps.get_model("product", "Product")
    for product in Product.objects.all():
        product.category = product.categories.first()
        product.save()


def assign_categories_to_products(apps, schema_editor):
    Product = apps.get_model("product", "Product")
    for product in Product.objects.all():
        if product.category:
            product.categories.add(product.category)


class Migration(migrations.Migration):

    dependencies = [("product", "0045_md_to_html")]

    operations = [
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="product.Category",
            ),
        ),
        migrations.RunPython(
            assign_category_to_products, assign_categories_to_products
        ),
    ]
