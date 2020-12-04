# Generated by Django 3.1.3 on 2020-12-03 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attribute", "0003_auto_20201113_1149"),
    ]

    operations = [
        migrations.AddField(
            model_name="attribute",
            name="entity_type",
            field=models.CharField(
                blank=True, choices=[("page", "Page")], max_length=50, null=True
            ),
        ),
        migrations.AlterField(
            model_name="attribute",
            name="input_type",
            field=models.CharField(
                choices=[
                    ("dropdown", "Dropdown"),
                    ("multiselect", "Multi Select"),
                    ("file", "File"),
                    ("reference", "Reference"),
                ],
                default="dropdown",
                max_length=50,
            ),
        ),
    ]
