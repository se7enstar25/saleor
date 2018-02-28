# Generated by Django 2.0.2 on 2018-02-28 00:54

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(db_index=True, max_length=100, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.", 'invalid')])),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_visible', models.BooleanField(default=False)),
                ('available_on', models.DateField(blank=True, null=True)),
            ],
            options={
                'ordering': ('url',),
                'permissions': (('view_page', 'Can view pages'), ('edit_page', 'Can edit pages')),
            },
        ),
    ]
