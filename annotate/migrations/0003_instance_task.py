# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotate', '0002_auto_20141113_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='instance',
            name='task',
            field=models.ForeignKey(default=1, to='annotate.Task'),
            preserve_default=False,
        ),
    ]
