# Generated by Django 3.2.2 on 2021-06-29 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0006_rewrite_auth_tokens"),
    ]

    operations = [
        migrations.AlterField(
            model_name="apptoken",
            name="raw_auth_token_last_4_chars",
            field=models.CharField(max_length=4),
        ),
    ]
