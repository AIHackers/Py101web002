# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-22 13:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WeatherData', '0002_auto_20170422_1253'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WeatherData',
            new_name='Data',
        ),
    ]
