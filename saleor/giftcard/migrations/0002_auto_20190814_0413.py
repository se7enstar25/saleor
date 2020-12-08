# Generated by Django 2.2.4 on 2019-08-14 09:13

import os

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("giftcard", "0001_initial")]

    operations = [
        migrations.RenameField(
            model_name="giftcard",
            old_name="current_balance",
            new_name="current_balance_amount",
        ),
        migrations.RenameField(
            model_name="giftcard",
            old_name="initial_balance",
            new_name="initial_balance_amount",
        ),
        migrations.AddField(
            model_name="giftcard",
            name="currency",
            field=models.CharField(
                default=os.environ.get("DEFAULT_CURRENCY", "USD"),
                max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH,
            ),
        ),
    ]
