# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotate', '0004_auto_20141113_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instance',
            name='text',
            field=models.CharField(max_length=1024),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='instancepool',
            name='name',
            field=models.CharField(max_length=256),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='instance',
            unique_together=set([('text', 'task')]),
        ),
        migrations.AlterUniqueTogether(
            name='instancepool',
            unique_together=set([('name', 'task')]),
        ),
    ]
