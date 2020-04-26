# Generated by Django 2.2.10 on 2020-02-17 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("discount", "0018_auto_20190827_0315"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="sale",
            options={
                "ordering": ("name", "pk"),
                "permissions": (("manage_discounts", "Manage sales and vouchers."),),
            },
        ),
        migrations.AlterModelOptions(
            name="saletranslation",
            options={"ordering": ("language_code", "name", "pk")},
        ),
        migrations.AlterModelOptions(name="voucher", options={"ordering": ("code",)},),
        migrations.AlterModelOptions(
            name="vouchercustomer", options={"ordering": ("voucher", "customer_email")},
        ),
        migrations.AlterModelOptions(
            name="vouchertranslation",
            options={"ordering": ("language_code", "voucher")},
        ),
    ]
