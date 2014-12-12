# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotate', '0003_instance_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='annotation',
            name='correct',
        ),
        migrations.AddField(
            model_name='annotation',
            name='value',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]
