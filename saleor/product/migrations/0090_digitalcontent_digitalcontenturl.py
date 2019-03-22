# Generated by Django 2.1.7 on 2019-03-22 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0089_auto_20190225_0252'),
    ]

    operations = [
        migrations.CreateModel(
            name='DigitalContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(choices=[('file', 'digital_product')], default='file', max_length=128)),
                ('content_file', models.FileField(blank=True, upload_to='digital_contents')),
                ('max_downloads', models.IntegerField(blank=True, null=True)),
                ('url_valid_days', models.IntegerField(blank=True, null=True)),
                ('product_variant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='digital_content', to='product.ProductVariant')),
            ],
        ),
        migrations.CreateModel(
            name='DigitalContentUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=36, unique=True)),
                ('valid_until', models.DateField(blank=True, null=True)),
                ('download_num', models.IntegerField(default=0)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urls', to='product.DigitalContent')),
            ],
        ),
    ]
