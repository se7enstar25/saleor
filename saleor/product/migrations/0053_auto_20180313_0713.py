# Generated by Django 2.0.3 on 2018-03-13 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0052_slug_field_length'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'permissions': (('view_category', 'Can view categories'), ('edit_category', 'Can edit categories')), 'verbose_name': 'Category'},
        ),
        migrations.AlterModelOptions(
            name='collection',
            options={'ordering': ['pk'], 'verbose_name': 'Collection'},
        ),
    ]
