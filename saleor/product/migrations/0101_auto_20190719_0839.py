# Generated by Django 2.2.3 on 2019-07-19 13:39

import django.contrib.postgres.fields.jsonb
from django.db import migrations
import saleor.core.utils.json_serializer


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0100_merge_20190719_0803'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=saleor.core.utils.json_serializer.CustomJsonEncoder, null=True),
        ),
        migrations.AddField(
            model_name='attribute',
            name='private_meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=saleor.core.utils.json_serializer.CustomJsonEncoder, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=saleor.core.utils.json_serializer.CustomJsonEncoder, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='private_meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=saleor.core.utils.json_serializer.CustomJsonEncoder, null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=saleor.core.utils.json_serializer.CustomJsonEncoder, null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='private_meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=saleor.core.utils.json_serializer.CustomJsonEncoder, null=True),
        ),
        migrations.AddField(
            model_name='digitalcontent',
            name='meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=saleor.core.utils.json_serializer.CustomJsonEncoder, null=True),
        ),
        migrations.AddField(
            model_name='digitalcontent',
            name='private_meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=saleor.core.utils.json_serializer.CustomJsonEncoder, null=True),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=saleor.core.utils.json_serializer.CustomJsonEncoder, null=True),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='private_meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=saleor.core.utils.json_serializer.CustomJsonEncoder, null=True),
        ),
    ]
