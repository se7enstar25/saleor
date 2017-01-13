# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-13 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('value', models.CharField(max_length=256, verbose_name='value')),
            ],
        ),
    ]
