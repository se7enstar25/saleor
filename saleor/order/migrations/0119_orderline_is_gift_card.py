# Generated by Django 3.2.6 on 2021-09-09 12:58

from django.db import migrations, models


def set_is_gift_card_field(apps, schema_editor):
    OrderLine = apps.get_model("order", "OrderLine")
    for line in OrderLine.objects.iterator():
        line.is_gift_card = (
            line.variant and line.variant.product.product_type.kind == "gift_card"
        )
        line.save()


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0118_auto_20210913_0731"),
        ("product", "0148_producttype_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderline",
            name="is_gift_card",
            field=models.BooleanField(null=True),
        ),
        migrations.RunPython(set_is_gift_card_field, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="orderline",
            name="is_gift_card",
            field=models.BooleanField(),
        ),
    ]
