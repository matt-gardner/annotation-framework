# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotate', '0005_auto_20141114_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='instancepool',
            name='selected',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
