# Generated by Django 2.2.10 on 2020-02-21 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0077_auto_20191118_0606"),
    ]

    operations = [
        migrations.RenameField(
            model_name="fulfillment",
            old_name="meta",
            new_name="metadata",
        ),
        migrations.RenameField(
            model_name="fulfillment",
            old_name="private_meta",
            new_name="private_metadata",
        ),
        migrations.RenameField(
            model_name="order",
            old_name="meta",
            new_name="metadata",
        ),
        migrations.RenameField(
            model_name="order",
            old_name="private_meta",
            new_name="private_metadata",
        ),
    ]
