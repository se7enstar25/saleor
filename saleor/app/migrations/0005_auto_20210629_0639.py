# Generated by Django 3.2.2 on 2021-06-29 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0004_auto_20210308_1135"),
    ]

    operations = [
        migrations.AddField(
            model_name="apptoken",
            name="raw_auth_token_last_4_chars",
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name="apptoken",
            name="auth_token",
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
