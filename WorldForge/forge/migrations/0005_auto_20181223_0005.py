# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-23 05:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forge', '0004_thing_tile'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image_credit',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='tile',
            name='image_credit',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='world',
            name='image_credit',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]