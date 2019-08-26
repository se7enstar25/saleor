# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-08 14:14
from __future__ import unicode_literals

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("order", "0026_auto_20171218_0428")]

    operations = [
        migrations.AlterField(
            model_name="deliverygroup",
            name="last_updated",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name="deliverygroup",
            name="shipping_method_name",
            field=models.CharField(
                blank=True, default=None, editable=False, max_length=255, null=True
            ),
        ),
        migrations.AlterField(
            model_name="deliverygroup",
            name="status",
            field=models.CharField(
                choices=[
                    ("new", "Processing"),
                    ("cancelled", "Cancelled"),
                    ("shipped", "Shipped"),
                ],
                default="new",
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name="deliverygroup",
            name="tracking_number",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AlterField(
            model_name="order",
            name="billing_address",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="account.Address",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="created",
            field=models.DateTimeField(
                default=django.utils.timezone.now, editable=False
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="discount_amount",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=12, null=True
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="discount_name",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AlterField(
            model_name="order",
            name="last_status_change",
            field=models.DateTimeField(
                default=django.utils.timezone.now, editable=False
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="shipping_address",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="account.Address",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="shipping_price",
            field=models.DecimalField(
                decimal_places=4, default=0, editable=False, max_digits=12
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="token",
            field=models.CharField(max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="total_net",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=12, null=True
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="total_tax",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=12, null=True
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="tracking_client_id",
            field=models.CharField(blank=True, editable=False, max_length=36),
        ),
        migrations.AlterField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="orders",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="user_email",
            field=models.EmailField(
                blank=True, default="", editable=False, max_length=254
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="voucher",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="discount.Voucher",
            ),
        ),
        migrations.AlterField(
            model_name="orderhistoryentry",
            name="comment",
            field=models.CharField(blank=True, default="", max_length=100),
        ),
        migrations.AlterField(
            model_name="orderhistoryentry",
            name="date",
            field=models.DateTimeField(
                default=django.utils.timezone.now, editable=False
            ),
        ),
        migrations.AlterField(
            model_name="orderhistoryentry",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="history",
                to="order.Order",
            ),
        ),
        migrations.AlterField(
            model_name="orderhistoryentry",
            name="status",
            field=models.CharField(
                choices=[("open", "Open"), ("closed", "Closed")], max_length=32
            ),
        ),
        migrations.AlterField(
            model_name="orderhistoryentry",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="orderline",
            name="delivery_group",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="lines",
                to="order.DeliveryGroup",
            ),
        ),
        migrations.AlterField(
            model_name="orderline",
            name="product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="product.Product",
            ),
        ),
        migrations.AlterField(
            model_name="orderline",
            name="product_name",
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name="orderline",
            name="product_sku",
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name="orderline",
            name="quantity",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(999),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="orderline",
            name="stock",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="product.Stock",
            ),
        ),
        migrations.AlterField(
            model_name="orderline",
            name="stock_location",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.AlterField(
            model_name="orderline",
            name="unit_price_gross",
            field=models.DecimalField(decimal_places=4, max_digits=12),
        ),
        migrations.AlterField(
            model_name="orderline",
            name="unit_price_net",
            field=models.DecimalField(decimal_places=4, max_digits=12),
        ),
        migrations.AlterField(
            model_name="ordernote",
            name="content",
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name="payment",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="payments",
                to="order.Order",
            ),
        ),
    ]
