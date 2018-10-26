# Generated by Django 2.1.2 on 2018-10-17 18:46

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django_prices.models
import saleor.core
from decimal import Decimal


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('checkout', '0015_auto_20181017_1346'),
        ('order', '0064_auto_20181016_0819'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gateway', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('charge_status', models.CharField(choices=[('charged', 'Charged'), ('not-charged', 'Not charged'), ('fully-refunded', 'Fully refunded')], default='not-charged', max_length=15)),
                ('billing_first_name', models.CharField(blank=True, max_length=256)),
                ('billing_last_name', models.CharField(blank=True, max_length=256)),
                ('billing_company_name', models.CharField(blank=True, max_length=256)),
                ('billing_address_1', models.CharField(blank=True, max_length=256)),
                ('billing_address_2', models.CharField(blank=True, max_length=256)),
                ('billing_city', models.CharField(blank=True, max_length=256)),
                ('billing_city_area', models.CharField(blank=True, max_length=128)),
                ('billing_postal_code', models.CharField(blank=True, max_length=256)),
                ('billing_country_code', models.CharField(blank=True, max_length=2)),
                ('billing_country_area', models.CharField(blank=True, max_length=256)),
                ('billing_email', models.EmailField(blank=True, max_length=254)),
                ('customer_ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('extra_data', models.TextField(blank=True, default='')),
                ('token', models.CharField(blank=True, default='', max_length=36)),
                ('currency', models.CharField(max_length=10)),
                ('total', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=12)),
                ('captured_amount', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=12)),
                ('checkout', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_methods', to='checkout.Cart')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='payment_methods', to='order.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('token', models.CharField(blank=True, default='', max_length=64)),
                ('kind', models.CharField(choices=[('auth', 'Authorization'), ('capture', 'Charge'), ('refund', 'Refund'), ('capture', 'Capture'), ('void', 'Void')], max_length=10)),
                ('is_success', models.BooleanField(default=False)),
                ('currency', models.CharField(max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=12)),
                ('gateway_response', django.contrib.postgres.fields.jsonb.JSONField()),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='payment.PaymentMethod')),
            ],
        ),
    ]
