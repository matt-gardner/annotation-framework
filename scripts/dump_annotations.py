#!/usr/bin/env python

import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'framework.settings'
sys.path.append('.')
sys.path.append('../')

import django
django.setup()
from annotate.models import Annotation



if __name__ == '__main__':
    outfile = 'data/annotations.tsv'
    out = open(outfile, 'w')
    for annotation in Annotation.objects.all():
        instance = annotation.instance
        user = annotation.user.username
        task = instance.task.name
        fields = [task, instance.text, user, annotation.value]
        out.write('\t'.join(fields) + '\n')
    out.close()

# vim: et sw=4 sts=4
