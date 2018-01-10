# Generated by Django 2.0.2 on 2018-02-21 16:56

from django.db import migrations
import django_prices.models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0033_auto_20180123_0832'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_gross',
            field=django_prices.models.MoneyField(blank=True, currency='USD', decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='orderline',
            name='unit_price_gross',
            field=django_prices.models.MoneyField(currency='USD', decimal_places=4, max_digits=12),
        ),
        migrations.AlterField(
            model_name='orderline',
            name='unit_price_net',
            field=django_prices.models.MoneyField(currency='USD', decimal_places=4, max_digits=12),
        ),
    ]
