# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-23 20:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotate', '0008_prediction_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prediction',
            name='info',
        ),
        migrations.AddField(
            model_name='instance',
            name='info',
            field=models.CharField(blank=True, max_length=1028),
        ),
    ]
