# Generated by Django 2.0.3 on 2018-03-22 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("order", "0042_auto_20180227_0436")]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={
                "ordering": ("-pk",),
                "permissions": (
                    ("view_order", "Can view orders"),
                    ("edit_order", "Can edit orders"),
                ),
            },
        ),
        migrations.AlterField(
            model_name="order",
            name="language_code",
            field=models.CharField(default="en", max_length=35),
        ),
    ]
