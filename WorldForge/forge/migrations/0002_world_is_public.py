# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-23 04:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forge', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='world',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
