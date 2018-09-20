# Generated by Django 2.0.8 on 2018-09-20 15:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0060_auto_20180919_0731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fulfillmentline',
            name='quantity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(999)]),
        ),
        migrations.AlterField(
            model_name='orderline',
            name='quantity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(999)]),
        ),
    ]
