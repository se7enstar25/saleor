# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-07 10:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site', '0008_auto_20171027_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorizationkey',
            name='name',
            field=models.CharField(choices=[('facebook', 'Facebook-Oauth2'), ('google-oauth2', 'Google-Oauth2')], max_length=20, verbose_name='name'),
        ),
    ]
