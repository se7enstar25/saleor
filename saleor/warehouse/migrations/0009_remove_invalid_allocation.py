# Generated by Django 3.0.6 on 2020-05-21 07:18

from django.db import migrations

DRAFT = "draft"
CANCELED = "canceled"


def remove_invalid_allocations(apps, schema_editor):
    Allocation = apps.get_model("warehouse", "Allocation")
    invalid_allocation = Allocation.objects.filter(
        order_line__order__status__in=[DRAFT, CANCELED]
    )
    invalid_allocation.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("warehouse", "0008_auto_20200430_0239"),
    ]

    operations = [
        migrations.RunPython(remove_invalid_allocations),
    ]
