# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-10 20:16
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='filters',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), default=list, help_text='Add items only if this words present in title or description', size=10),
        ),
        migrations.AddField(
            model_name='feed',
            name='rss_modified',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='feed',
            name='rss_title',
            field=models.CharField(default='', max_length=500),
        ),
    ]
