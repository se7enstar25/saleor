# Generated by Django 2.0.3 on 2018-08-13 13:14

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0051_merge_20180807_0704'),
        ('checkout', '0009_cart_translated_discount_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('charge_status', models.CharField(choices=[('charged', 'Charged'), ('not-charged', 'Not charged'), ('fully-refunded', 'Fully refunded')], default='not-charged', max_length=15)),
                ('billing_first_name', models.CharField(blank=True, max_length=256)),
                ('billing_last_name', models.CharField(blank=True, max_length=256)),
                ('billing_address_1', models.CharField(blank=True, max_length=256)),
                ('billing_address_2', models.CharField(blank=True, max_length=256)),
                ('billing_city', models.CharField(blank=True, max_length=256)),
                ('billing_postcode', models.CharField(blank=True, max_length=256)),
                ('billing_country_code', models.CharField(blank=True, max_length=2)),
                ('billing_country_area', models.CharField(blank=True, max_length=256)),
                ('billing_email', models.EmailField(blank=True, max_length=254)),
                ('customer_ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('extra_data', models.TextField(blank=True, default='')),
                ('token', models.CharField(blank=True, default='', max_length=36)),
                ('total', models.DecimalField(decimal_places=2, default='0.0', max_digits=9)),
                ('currency', models.CharField(max_length=10)),
                ('captured_amount', models.DecimalField(decimal_places=2, default='0.0', max_digits=9)),
                ('tax', models.DecimalField(decimal_places=2, default='0.0', max_digits=9)),
                ('checkout', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_methods', to='checkout.Cart')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_methods', to='order.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, default='', max_length=64)),
                ('transaction_type', models.CharField(choices=[('auth', 'Authorization'), ('charge', 'Charge'), ('refund', 'Refund'), ('void', 'Void')], max_length=10)),
                ('is_success', models.BooleanField(default=False)),
                ('total', models.DecimalField(decimal_places=2, default='0.0', max_digits=9)),
                ('currency', models.CharField(max_length=10)),
                ('captured_amount', models.DecimalField(decimal_places=2, default='0.0', max_digits=9)),
                ('tax', models.DecimalField(decimal_places=2, default='0.0', max_digits=9)),
                ('gateway_response', jsonfield.fields.JSONField()),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='checkout.PaymentMethod')),
            ],
        ),
    ]
