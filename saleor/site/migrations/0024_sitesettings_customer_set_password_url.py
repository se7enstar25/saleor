# Generated by Django 2.2.6 on 2019-10-21 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("site", "0023_auto_20191007_0835")]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="customer_set_password_url",
            field=models.CharField(blank=True, max_length=255, null=True),
        )
    ]
