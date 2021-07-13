# Generated by Django 3.2.2 on 2021-05-14 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0107_set_origin_and_original_values"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="origin",
            field=models.CharField(
                choices=[
                    ("checkout", "Checkout"),
                    ("draft", "Draft"),
                    ("reissue", "Reissue"),
                ],
                max_length=32,
            ),
        ),
    ]
