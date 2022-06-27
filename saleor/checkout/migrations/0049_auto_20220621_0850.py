# Generated by Django 3.2.13 on 2022-06-21 08:50

import django.contrib.postgres.indexes
from django.db import migrations, models
import saleor.core.utils.json_serializer


class Migration(migrations.Migration):

    dependencies = [
        ("checkout", "0048_alter_checkoutline_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="checkoutline",
            name="metadata",
            field=models.JSONField(
                blank=True,
                default=dict,
                encoder=saleor.core.utils.json_serializer.CustomJsonEncoder,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="checkoutline",
            name="private_metadata",
            field=models.JSONField(
                blank=True,
                default=dict,
                encoder=saleor.core.utils.json_serializer.CustomJsonEncoder,
                null=True,
            ),
        ),
        migrations.AddIndex(
            model_name="checkoutline",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["private_metadata"], name="checkoutline_p_meta_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="checkoutline",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["metadata"], name="checkoutline_meta_idx"
            ),
        ),
    ]
