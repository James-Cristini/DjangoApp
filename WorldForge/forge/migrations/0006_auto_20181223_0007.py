# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-23 05:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forge', '0005_auto_20181223_0005'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='story',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='thing',
            name='story',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='tile',
            name='story',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='world',
            name='story',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='thing',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='tile',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='world',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='world',
            name='genre',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]