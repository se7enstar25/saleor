# Generated by Django 3.1.2 on 2020-10-14 08:16

from django.db import migrations, models
from django.db.models.functions import Lower
from django.utils.text import slugify


def create_unique_slugs_for_menus(apps, schema_editor):
    Menu = apps.get_model("menu", "Menu")

    menus = Menu.objects.filter(slug__isnull=True).order_by(Lower("name")).iterator()
    previous_char = ""
    slug_values = []
    for menu in menus:
        first_char = menu.name[0].lower()
        if first_char != previous_char:
            previous_char = first_char
            slug_values = list(
                Menu.objects.filter(slug__istartswith=first_char).values_list(
                    "slug", flat=True
                )
            )

        slug = generate_unique_slug(menu, slug_values)
        menu.slug = slug
        menu.save(update_fields=["slug"])
        slug_values.append(slug)


def generate_unique_slug(instance, slug_values_list):
    slug = slugify(instance.name)
    unique_slug = slug

    extension = 1

    while unique_slug in slug_values_list:
        extension += 1
        unique_slug = f"{slug}-{extension}"

    return unique_slug


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0018_auto_20200709_1102"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menu",
            name="name",
            field=models.CharField(max_length=250),
        ),
        # Temporary set the slug "null" to True to allow slug generation to run.
        migrations.AddField(
            model_name="menu",
            name="slug",
            field=models.SlugField(
                allow_unicode=True, max_length=255, unique=True, null=True
            ),
            preserve_default=False,
        ),
        migrations.RunPython(create_unique_slugs_for_menus, migrations.RunPython.noop),
        # Set "null" of slug back to False as reflected in model.
        migrations.AlterField(
            model_name="menu",
            name="slug",
            field=models.SlugField(
                allow_unicode=True, max_length=255, unique=True, null=False
            ),
        ),
    ]
