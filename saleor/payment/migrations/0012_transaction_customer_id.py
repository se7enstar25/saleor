# Generated by Django 2.2.2 on 2019-06-28 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0011_auto_20190516_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='customer_id',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
