# Generated by Django 2.2.3 on 2019-07-19 12:45

import django.contrib.postgres.fields.jsonb
from django.db import migrations

import saleor.core.utils.json_serializer


class Migration(migrations.Migration):

    dependencies = [("account", "0030_auto_20190719_0733")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="private_meta",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                blank=True,
                default=dict,
                encoder=saleor.core.utils.json_serializer.CustomJsonEncoder,
                null=True,
            ),
        )
    ]
