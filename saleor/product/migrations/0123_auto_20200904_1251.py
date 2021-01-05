# Generated by Django 3.1 on 2020-09-04 12:51

from django.db import migrations
from django.db.models import Count


def remove_variant_image_duplicates(apps, schema_editor):
    ProductImage = apps.get_model("product", "ProductImage")
    VariantImage = apps.get_model("product", "VariantImage")

    duplicated_images = (
        ProductImage.objects.values("pk", "variant_images__variant")
        .annotate(variant_count=Count("variant_images__variant"))
        .filter(variant_count__gte=2)
    )

    variant_image_ids_to_remove = []
    for image_data in duplicated_images:
        ids = VariantImage.objects.filter(
            variant=image_data["variant_images__variant"],
            image__pk=image_data["pk"],
        )[1:].values_list("pk", flat=True)
        variant_image_ids_to_remove += ids

    VariantImage.objects.filter(pk__in=variant_image_ids_to_remove).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0122_auto_20200828_1135"),
    ]

    operations = [
        migrations.RunPython(
            remove_variant_image_duplicates, migrations.RunPython.noop
        ),
        migrations.AlterUniqueTogether(
            name="variantimage",
            unique_together={("variant", "image")},
        ),
    ]
