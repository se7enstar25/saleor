# Generated by Django 3.2.13 on 2022-05-16 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("checkout", "0047_merge_20220519_1029"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="checkoutline",
            options={"ordering": ("created_at", "id")},
        ),
    ]
