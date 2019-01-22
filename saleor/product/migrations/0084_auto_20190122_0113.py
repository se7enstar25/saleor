# Generated by Django 2.1.4 on 2019-01-22 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0083_auto_20190104_0443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tax_rate',
            field=models.CharField(blank=True, choices=[('accommodation', 'accommodation'), ('admission to cultural events', 'admission to cultural events'), ('admission to entertainment events', 'admission to entertainment events'), ('admission to sporting events', 'admission to sporting events'), ('advertising', 'advertising'), ('agricultural supplies', 'agricultural supplies'), ('baby foodstuffs', 'baby foodstuffs'), ('bikes', 'bikes'), ('books', 'books'), ('childrens clothing', 'childrens clothing'), ('domestic fuel', 'domestic fuel'), ('domestic services', 'domestic services'), ('e-books', 'e-books'), ('foodstuffs', 'foodstuffs'), ('hotels', 'hotels'), ('medical', 'medical'), ('newspapers', 'newspapers'), ('passenger transport', 'passenger transport'), ('pharmaceuticals', 'pharmaceuticals'), ('property renovations', 'property renovations'), ('restaurants', 'restaurants'), ('social housing', 'social housing'), ('standard', 'standard'), ('water', 'water'), ('wine', 'wine')], default='standard', max_length=128),
        ),
        migrations.AlterField(
            model_name='producttype',
            name='tax_rate',
            field=models.CharField(choices=[('accommodation', 'accommodation'), ('admission to cultural events', 'admission to cultural events'), ('admission to entertainment events', 'admission to entertainment events'), ('admission to sporting events', 'admission to sporting events'), ('advertising', 'advertising'), ('agricultural supplies', 'agricultural supplies'), ('baby foodstuffs', 'baby foodstuffs'), ('bikes', 'bikes'), ('books', 'books'), ('childrens clothing', 'childrens clothing'), ('domestic fuel', 'domestic fuel'), ('domestic services', 'domestic services'), ('e-books', 'e-books'), ('foodstuffs', 'foodstuffs'), ('hotels', 'hotels'), ('medical', 'medical'), ('newspapers', 'newspapers'), ('passenger transport', 'passenger transport'), ('pharmaceuticals', 'pharmaceuticals'), ('property renovations', 'property renovations'), ('restaurants', 'restaurants'), ('social housing', 'social housing'), ('standard', 'standard'), ('water', 'water'), ('wine', 'wine')], default='standard', max_length=128),
        ),
    ]
