# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-11 09:09
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0005_auto_20170411_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='filters',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, default=list, help_text='Comma separated.Add items only if one of this words present in feed title or description', size=10),
        ),
    ]
