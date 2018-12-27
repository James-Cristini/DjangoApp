# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-27 02:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forge', '0012_auto_20181225_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='thing',
            name='image_thumb',
            field=models.ImageField(default='default_thing.jpg', upload_to='thing_images/thumbs'),
        ),
        migrations.AddField(
            model_name='tile',
            name='image_thumb',
            field=models.ImageField(default='default_tile.jpg', upload_to='tile_images/thumbs'),
        ),
        migrations.AddField(
            model_name='world',
            name='image_thumb',
            field=models.ImageField(default='default_world.jpg', upload_to='world_images/thumbs'),
        ),
    ]
