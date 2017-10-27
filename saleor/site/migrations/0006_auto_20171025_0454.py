# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 09:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('site', '0005_auto_20170906_0556'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='site',
            field=models.OneToOneField(blank=True,
                                       on_delete=django.db.models.deletion.CASCADE,
                                       related_name='settings',
                                       to='sites.Site'),
            preserve_default=False,
        ),
    ]
