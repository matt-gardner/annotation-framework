#!/usr/bin/env python

import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'framework.settings'
sys.path.append('.')
sys.path.append('../')

from collections import defaultdict

import django
django.setup()
from django.db import transaction
from annotate.models import Instance
from annotate.models import InstancePool
from annotate.models import Task


def main(k):
    transaction.set_autocommit(False)
    method_task_instances = defaultdict(lambda: defaultdict(list))
    task_names = set()
    for filename in os.listdir('data/filtered'):
        for line in open('data/filtered/' + filename):
            fields = line.split('\t')
            task = fields[0]
            method = fields[1]
            rank = int(fields[2])
            instance = fields[3]
            if rank <= k:
                method_task_instances[method][task].append((rank, instance))
            task_names.add(task)
    for t in task_names:
        task = Task.objects.get(name=t)
        pool_name = 'Top %d for predicate %s' % (k, t)
        pool = InstancePool(task=task, name=pool_name, selected=True)
        pool.save()
        for method in method_task_instances:
            instances = method_task_instances[method][t]
            instances.sort()
            instances = [x[1] for x in instances]
            add_top_k_to_pool(instances, task, pool, k)
    transaction.commit()
    transaction.set_autocommit(True)


def add_top_k_to_pool(instances, task, pool, k):
    for instance_text in instances[:k]:
        instance = Instance.objects.get(task=task, text=instance_text)
        pool.instances.add(instance)


if __name__ == '__main__':
    main(25)

# vim: et sw=4 sts=4
