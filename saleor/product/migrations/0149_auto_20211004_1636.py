# Generated by Django 3.2.6 on 2021-10-04 16:36

import django.contrib.postgres.indexes
from django.db import migrations, models


def parse_draftjs_content_to_string(definitions):
    string = ""
    blocks = definitions.get("blocks")
    if not blocks or not isinstance(blocks, list):
        return ""
    for block in blocks:
        text = block.get("text")
        if not text:
            continue
        string += f"{text} "

    return string


def parse_description_json_field(apps, schema):
    Category = apps.get_model("product", "Category")

    for category in Category.objects.iterator():
        category.description_plaintext = parse_draftjs_content_to_string(
            category.description
        )
        category.save(update_fields=["description_plaintext"])


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0148_producttype_product_type_search_gin"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="description_plaintext",
            field=models.TextField(blank=True),
        ),
        migrations.AddIndex(
            model_name="category",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["name", "slug", "description_plaintext"],
                name="category_search_name_slug_gin",
                opclasses=["gin_trgm_ops", "gin_trgm_ops", "gin_trgm_ops"],
            ),
        ),
        migrations.RunPython(
            parse_description_json_field,
            migrations.RunPython.noop,
        ),
    ]
