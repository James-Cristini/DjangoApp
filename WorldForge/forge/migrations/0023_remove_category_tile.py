# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-01 20:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forge', '0022_auto_20190101_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='tile',
        ),
    ]
