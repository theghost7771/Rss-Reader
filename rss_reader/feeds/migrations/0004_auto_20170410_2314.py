# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-10 23:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0003_auto_20170410_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feeditem',
            name='description',
            field=models.CharField(max_length=2000),
        ),
    ]
