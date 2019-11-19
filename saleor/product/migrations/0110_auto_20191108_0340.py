# Generated by Django 2.2.6 on 2019-11-08 09:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("product", "0109_auto_20191006_1433")]

    operations = [
        migrations.AlterField(
            model_name="collection",
            name="is_published",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="products",
                to="product.Category",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="is_published",
            field=models.BooleanField(default=False),
        ),
    ]
