# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 10:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0031_auto_20170206_0601'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attributechoicevalue',
            unique_together=set([('display', 'attribute')]),
        ),
    ]
