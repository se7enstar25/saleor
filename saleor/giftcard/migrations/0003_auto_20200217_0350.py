# Generated by Django 2.2.10 on 2020-02-17 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("giftcard", "0002_auto_20190814_0413"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="giftcard",
            options={
                "ordering": ("code",),
                "permissions": (("manage_gift_card", "Manage gift cards."),),
            },
        ),
    ]
