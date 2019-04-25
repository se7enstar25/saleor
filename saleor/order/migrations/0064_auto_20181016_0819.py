# Generated by Django 2.1.2 on 2018-10-16 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0063_auto_20180926_0446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderline',
            name='variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_lines', to='product.ProductVariant'),
        ),
    ]
