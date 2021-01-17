# Generated by Django 2.2.9 on 2020-01-23 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("warehouse", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="warehouse",
            name="company_name",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="warehouse",
            name="email",
            field=models.EmailField(blank=True, default="", max_length=254),
        ),
        migrations.AlterField(
            model_name="warehouse",
            name="name",
            field=models.CharField(max_length=255),
        ),
    ]
