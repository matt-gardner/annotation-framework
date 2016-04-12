#!/usr/bin/env python

import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'framework.settings'
sys.path.append('.')
sys.path.append('../')

from collections import defaultdict
import random

import django
django.setup()
from django.db import transaction
from annotate.models import Instance
from annotate.models import InstancePool
from annotate.models import Method
from annotate.models import Prediction
from annotate.models import Task


@transaction.atomic
def main(data_file, method_name):
    #transaction.set_autocommit(False)
    method = Method(name=method_name)
    method.save()
    tasks = {}
    task_instances = defaultdict(list)
    for line in open(data_file):
        fields = line.split('\t')
        task_name = fields[0]
        rank = int(fields[2])
        text = fields[3]
        task = get_task_from_name(tasks, task_name)
        instance = get_instance(text, task)
        task_instances[task].append(instance)
        instance.save()
        prediction = Prediction(method=method,
                                task=task,
                                instance=instance,
                                ranking=rank)
        prediction.save()
    sample_instances_for_pool(task_instances)
    #transaction.commit()
    #transaction.set_autocommit(True)


def get_instance(text, task):
    try:
        return Instance.objects.get(text=text, task=task)
    except Instance.DoesNotExist:
        instance = Instance(text=text, task=task)
        instance.save()
        return instance


def get_task_from_name(tasks, task_name):
    task = tasks.get(task_name, None)
    if not task:
        try:
            task = Task.objects.get(name=task_name)
        except Task.DoesNotExist:
            task = Task(name=task_name)
            task.save()
        tasks[task_name] = task
    return task


def sample_instances_for_pool(task_instances):
    k = [0, 10, 100, 1000]
    m = 20
    for task in task_instances:
        pool_name = 'top k pool (k=' + str(k[1:]) + '; m=' + str(m) + ')'
        try:
            pool = InstancePool.objects.get(name=pool_name, task=task)
        except InstancePool.DoesNotExist:
            pool = InstancePool(name=pool_name, task=task, selected=False)
            pool.save()
        for i in range(len(k)-1):
            instances = task_instances[task][k[i]:k[i+1]]
            random.shuffle(instances)
            add_instances_to_pool(instances[:m], pool)


def add_instances_to_pool(instances, pool):
    for instance in instances:
        pool.instances.add(instance)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

# vim: et sw=4 sts=4
