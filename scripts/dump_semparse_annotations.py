#!/usr/bin/env python

import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'framework.settings'
sys.path.append('.')
sys.path.append('../')

import django
django.setup()
from annotate.models import Task



if __name__ == '__main__':
    outfile = 'finished_annotations.tsv'
    out = open(outfile, 'w')
    for task in Task.objects.all():
        instances = task.instance_set.all()
        out.write('\n')
        out.write(task.name)
        out.write('\n')
        annotated = []
        for instance in instances:
            annotations = instance.annotation_set.all()
            if len(annotations) == 1:
                annotation = annotations[0]
                valueIndex = 0 if annotation.value == 'correct' else 2
            else:
                valueIndex = 1
            annotated.append((valueIndex, instance))
        annotated.sort()
        for (valueIndex, instance) in annotated:
            if valueIndex == 0:
                value = '1'
            elif valueIndex == 1:
                value = '?'
            else:
                value = '0'
            out.write(value)
            out.write(' ')
            out.write(instance.text)
            out.write(' ')
            out.write('http://www.freebase.com')
            out.write(instance.text)
            out.write(' ')
            out.write(instance.info.encode('utf-8'))
            out.write('\n')
    out.close()

# vim: et sw=4 sts=4
