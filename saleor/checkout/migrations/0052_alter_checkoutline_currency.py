# Generated by Django 3.2.14 on 2022-07-13 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("checkout", "0051_auto_20220713_1103"),
    ]

    operations = [
        migrations.AlterField(
            model_name="checkoutline",
            name="currency",
            field=models.CharField(max_length=3),
        ),
    ]
