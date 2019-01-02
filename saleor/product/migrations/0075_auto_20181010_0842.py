# Generated by Django 2.1.2 on 2018-10-10 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0074_auto_20181010_0730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producttype',
            name='product_attributes',
        ),
        migrations.RemoveField(
            model_name='producttype',
            name='variant_attributes',
        ),
        migrations.AlterField(
            model_name='attribute',
            name='product_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_attributes', to='product.ProductType'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='product_variant_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variant_attributes', to='product.ProductType'),
        ),
    ]
