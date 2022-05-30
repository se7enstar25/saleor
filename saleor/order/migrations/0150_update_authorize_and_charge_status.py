# Generated by Django 3.2.13 on 2022-05-19 11:21

from django.db import migrations, models


def update_authorize_status(apps, _schema_editor):
    Order = apps.get_model("order", "Order")
    order_query = Order.objects.annotate(
        sum_authorized=models.F("total_authorized_amount")
        + models.F("total_charged_amount")
    )
    order_query.filter(
        sum_authorized__gt=0, sum_authorized__lt=models.F("total_gross_amount")
    ).update(authorize_status="partial")
    order_query.filter(sum_authorized__gte=models.F("total_gross_amount")).update(
        authorize_status="full"
    )


def update_charge_status(apps, _schema_editor):
    Order = apps.get_model("order", "Order")
    Order.objects.filter(
        total_charged_amount__gt=0,
        total_charged_amount__lt=models.F("total_gross_amount"),
    ).update(charge_status="partial")

    Order.objects.filter(total_charged_amount=models.F("total_gross_amount")).update(
        charge_status="full"
    )
    Order.objects.filter(
        total_charged_amount__gt=models.F("total_gross_amount")
    ).update(charge_status="overcharged")


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0149_add_fields_for_authorize_and_charge"),
    ]

    operations = [
        migrations.RunPython(
            update_authorize_status, reverse_code=migrations.RunPython.noop
        ),
        migrations.RunPython(
            update_charge_status, reverse_code=migrations.RunPython.noop
        ),
    ]
