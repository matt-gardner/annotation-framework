#!/usr/bin/env python

import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'framework.settings'
sys.path.append('.')
sys.path.append('../')

from collections import defaultdict
from collections import namedtuple
import random

import django
django.setup()
from django.db import transaction
from django.contrib.auth.models import User
from annotate.models import Annotation
from annotate.models import Instance
from annotate.models import InstancePool
from annotate.models import Method
from annotate.models import Prediction
from annotate.models import Task


@transaction.atomic
def main(data_file):
    method_name = "All of them (Jayant's script already grouped the predictions)"
    try:
        method = Method.objects.get(name=method_name)
    except Method.DoesNotExist:
        method = Method(name=method_name)
        method.save()
    tasks = {}
    task_instances = defaultdict(list)
    pool_name = 'All instances'
    create_user('matt')
    user = create_user('pre-existing')
    to_annotate = read_to_annotate_file(data_file)
    for (sentence, logical_form, pred) in to_annotate:
        task_name = sentence + '\n' + logical_form
        rank = 0
        text = pred.mid
        task = get_task_from_name(tasks, task_name)
        instance = get_instance(text, task, pred.name)
        task_instances[task].append(instance)
        instance.save()
        prediction = Prediction(method=method,
                                task=task,
                                instance=instance,
                                ranking=rank)
        prediction.save()
        try:
            pool = InstancePool.objects.get(name=pool_name, task=task)
        except InstancePool.DoesNotExist:
            pool = InstancePool(name=pool_name, task=task, selected=True)
            pool.save()
        pool.instances.add(instance)
        if pred.annotation != '?':
            value = 'correct' if pred.annotation == '1' else 'incorrect'
            annotation = Annotation(instance=instance, user=user, value=value)
            annotation.save()


def read_to_annotate_file(filename):
    sentence = None
    logical_form = None
    predictions = []
    to_annotate = []
    for line in open(filename):
        if line == '\n':
            if sentence:
                to_annotate.extend([(sentence, logical_form, pred) for pred in predictions])
            sentence = None
            logical_form = None
            predictions = []
        elif line.startswith('(lambda '):
            logical_form = line.strip()
        elif line.startswith('1 /') or line.startswith('? /') or line.startswith('0 /'):
            predictions.append(process_prediction(line.strip()))
        else:
            sentence = line.strip()
    return to_annotate


PredTuple = namedtuple('PredTuple', ['annotation', 'mid', 'url', 'name'])
def process_prediction(line):
    fields = line.split()
    annotation = fields[0]
    mid = fields[1]
    url = fields[2]
    name = ' '.join(fields[3:])
    print annotation, mid, url, name
    return PredTuple(annotation, mid, url, name)



def get_instance(text, task, info):
    try:
        return Instance.objects.get(text=text, task=task, info=info)
    except Instance.DoesNotExist:
        instance = Instance(text=text, task=task, info=info)
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


def create_user(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User(username=username)
        user.set_password(username)
        user.save()
    return user

if __name__ == '__main__':
    main(sys.argv[1])

# vim: et sw=4 sts=4
