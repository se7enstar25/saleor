# Generated by Django 2.2.3 on 2019-07-04 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("discount", "0014_auto_20190701_0402")]

    operations = [
        migrations.AddField(
            model_name="voucher",
            name="min_checkout_items_quantity",
            field=models.PositiveIntegerField(blank=True, null=True),
        )
    ]
