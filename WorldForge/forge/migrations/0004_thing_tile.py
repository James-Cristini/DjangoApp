# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-23 04:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forge', '0003_auto_20181222_2334'),
    ]

    operations = [
        migrations.AddField(
            model_name='thing',
            name='tile',
            field=models.ManyToManyField(blank=True, to='forge.Tile'),
        ),
    ]