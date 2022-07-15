# Generated by Django 3.2.13 on 2022-06-13 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0170_rewrite_digitalcontenturl_orderline_relation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="background_image",
            field=models.ImageField(
                blank=True, null=True, upload_to="category-backgrounds"
            ),
        ),
        migrations.AlterField(
            model_name="collection",
            name="background_image",
            field=models.ImageField(
                blank=True, null=True, upload_to="collection-backgrounds"
            ),
        ),
        migrations.RemoveField(
            model_name="productmedia",
            name="ppoi",
        ),
        migrations.AlterField(
            model_name="productmedia",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="products"),
        ),
    ]
