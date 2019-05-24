# Generated by Django 2.1.3 on 2018-11-26 14:25

from django.db import migrations, models

from ...core.taxes.vatlayer import DEFAULT_TAX_RATE_NAME


def add_default_tax_rate_instead_of_empty_field(apps, schema_editor):
    ProductType = apps.get_model("product", "ProductType")
    product_types = ProductType.objects.filter(tax_rate="")
    product_types.update(tax_rate=DEFAULT_TAX_RATE_NAME)


class Migration(migrations.Migration):

    dependencies = [("product", "0078_auto_20181120_0437")]

    operations = [
        migrations.AlterField(
            model_name="producttype",
            name="tax_rate",
            field=models.CharField(
                choices=[
                    ("accommodation", "accommodation"),
                    ("admission to cultural events", "admission to cultural events"),
                    (
                        "admission to entertainment events",
                        "admission to entertainment events",
                    ),
                    ("admission to sporting events", "admission to sporting events"),
                    ("advertising", "advertising"),
                    ("agricultural supplies", "agricultural supplies"),
                    ("baby foodstuffs", "baby foodstuffs"),
                    ("bikes", "bikes"),
                    ("books", "books"),
                    ("childrens clothing", "childrens clothing"),
                    ("domestic fuel", "domestic fuel"),
                    ("domestic services", "domestic services"),
                    ("e-books", "e-books"),
                    ("foodstuffs", "foodstuffs"),
                    ("hotels", "hotels"),
                    ("medical", "medical"),
                    ("newspapers", "newspapers"),
                    ("passenger transport", "passenger transport"),
                    ("pharmaceuticals", "pharmaceuticals"),
                    ("property renovations", "property renovations"),
                    ("restaurants", "restaurants"),
                    ("social housing", "social housing"),
                    ("standard", "standard"),
                    ("water", "water"),
                ],
                default="standard",
                max_length=128,
            ),
        ),
        migrations.RunPython(add_default_tax_rate_instead_of_empty_field),
    ]
