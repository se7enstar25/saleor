# Generated by Django 2.1.7 on 2019-03-26 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site', '0020_auto_20190301_0336'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='automatic_fulfillment_digital_products',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='default_digital_max_downloads',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='default_digital_url_valid_days',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
