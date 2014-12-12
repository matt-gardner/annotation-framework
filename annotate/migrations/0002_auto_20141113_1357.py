# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instance',
            name='text',
            field=models.CharField(unique=True, max_length=1024),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='instancepool',
            name='name',
            field=models.CharField(unique=True, max_length=256),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='method',
            name='name',
            field=models.CharField(unique=True, max_length=256),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(unique=True, max_length=256),
            preserve_default=True,
        ),
    ]
