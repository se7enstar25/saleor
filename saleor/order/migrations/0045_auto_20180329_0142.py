# Generated by Django 2.0.3 on 2018-03-29 06:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_prices.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0054_merge_20180320_1108'),
        ('order', '0044_auto_20180326_1055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderline',
            name='stock',
        ),
        migrations.RemoveField(
            model_name='orderline',
            name='stock_location',
        ),
        migrations.AddField(
            model_name='orderline',
            name='variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='product.ProductVariant'),
        ),
        migrations.RemoveField(
            model_name='orderline',
            name='product',
        ),
        migrations.AlterField(
            model_name='orderline',
            name='unit_price_gross',
            field=django_prices.models.MoneyField(currency=settings.DEFAULT_CURRENCY, decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='orderline',
            name='unit_price_net',
            field=django_prices.models.MoneyField(currency=settings.DEFAULT_CURRENCY, decimal_places=2, max_digits=12),
        ),
    ]
