# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-24 16:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotate', '0009_auto_20160223_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='assigned',
            field=models.BooleanField(default=False),
        ),
    ]
