# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-26 04:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forge', '0010_thing_image_credit'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='thing',
            options={'ordering': ('str_name',)},
        ),
        migrations.AddField(
            model_name='thing',
            name='str_name',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]