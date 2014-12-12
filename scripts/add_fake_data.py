#!/usr/bin/env python

import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'framework.settings'
sys.path.append('.')
sys.path.append('../')

import django
django.setup()
from django.db import transaction
from annotate.models import Annotation
from annotate.models import Instance
from annotate.models import InstancePool
from annotate.models import Method
from annotate.models import Prediction
from annotate.models import Task


def main():
    transaction.set_autocommit(False)
    clear_db()
    task = Task(name="category:fake_animal")
    task.save()
    method = Method(name="NELL iteration -1")
    method.save()
    for i in range(1, 10000):
        instance = Instance(text="entity " + str(i), task=task)
        instance.save()
        prediction = Prediction(method=method,
                                task=task,
                                instance=instance,
                                ranking=i)
        prediction.save()
    pool = InstancePool(name='top k', task=task)
    pool.save()
    sample_instances_for_pool(method, task, pool)
    transaction.commit()
    transaction.set_autocommit(True)


def sample_instances_for_pool(method, task, pool):
    instances = task.instance_set.all()
    for instance in instances[:100]:
        pool.instances.add(instance)


def clear_db():
    while Task.objects.count():
        ids = Task.objects.values_list('pk', flat=True)[:100]
        Task.objects.filter(pk__in = ids).delete()
    Method.objects.all().delete()
    while Instance.objects.count():
        ids = Instance.objects.values_list('pk', flat=True)[:100]
        Instance.objects.filter(pk__in = ids).delete()
    while InstancePool.objects.count():
        ids = InstancePool.objects.values_list('pk', flat=True)[:100]
        InstancePool.objects.filter(pk__in = ids).delete()
    while Prediction.objects.count():
        ids = Prediction.objects.values_list('pk', flat=True)[:100]
        Prediction.objects.filter(pk__in = ids).delete()
    while Annotation.objects.count():
        ids = Annotation.objects.values_list('pk', flat=True)[:100]
        Annotation.objects.filter(pk__in = ids).delete()


if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
