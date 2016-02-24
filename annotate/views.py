from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from annotate.models import Annotation
from annotate.models import Instance
from annotate.models import InstancePool
from annotate.models import Method
from annotate.models import Prediction
from annotate.models import Task

from collections import defaultdict
from collections import namedtuple

import random

def home(request):
    context = base_context()
    context['methods'] = Method.objects.all()
    TaskTuple = namedtuple('TaskTuple',
                           ['name', 'id', 'to_annotate', 'annotated', 'user'])
    tasks = []
    annotated_instances = set(
            Annotation.objects.values_list('instance_id', flat=True))
    pool_instances = defaultdict(list)
    for i in InstancePool.instances.through.objects.all():
        pool_instances[i.instancepool_id].append(i.instance_id)
    for task in Task.objects.all():
        instances = set()
        annotated = set()
        selected = False
        for pool in task.instancepool_set.all():
            if not pool.selected: continue
            selected = True
            for instance in pool_instances[pool.id]:
                instances.add(instance)
                if instance in annotated_instances:
                    annotated.add(instance)
        if not selected: continue
        user = task.assignedTo.username if task.assignedTo else ''
        tasks.append(TaskTuple(name=task.name,
                               id=task.id,
                               to_annotate=len(instances) - len(annotated),
                               annotated=len(annotated),
                               user=user))
    tasks.sort(key=lambda x: (-x.to_annotate, x.name))
    context['tasks'] = tasks
    context['total_tasks'] = len(tasks)
    context['total_annotations'] = Annotation.objects.count
    context['total_instances'] = Instance.objects.count
    context['total_left_to_annotate'] = len(Instance.objects.filter(annotation__isnull=True))
    return render(request, "main.html", context)


def method(request, method_id):
    context = base_context()
    method = get_object_or_404(Method, pk=method_id)
    context['method'] = method
    context['tasks'] = Task.objects.all()
    return render(request, "method.html", context)


def method_task(request, method_id, task_id):
    context = base_context()
    method = get_object_or_404(Method, pk=method_id)
    task = get_object_or_404(Task, pk=task_id)
    context['method'] = method
    context['task'] = task
    InstanceTuple = namedtuple('InstanceTuple',
                               ['text', 'id', 'annotations', 'conflict'])
    AnnotationTuple = namedtuple('AnnotationTuple', ['user', 'value'])
    predictions = []
    for prediction in Prediction.objects.filter(method=method, task=task):
        instance = prediction.instance
        annotations = []
        for annotation in instance.annotation_set.all():
            annotations.append(AnnotationTuple(annotation.user.username,
                                               annotation.value))
        distinct_annotations = len(set([x.value for x in annotations]))
        conflict = False
        if distinct_annotations > 1:
            conflict = True
        predictions.append(InstanceTuple(instance.text,
                                         instance.id,
                                         annotations,
                                         conflict))
    context['predictions'] = predictions
    return render(request, "method_task.html", context)


@login_required
def task(request, task_id):
    context = base_context()
    task = get_object_or_404(Task, pk=task_id)
    context['task'] = task
    context['pools'] = task.instancepool_set.filter(~Q(name__contains='(old)'))
    context['username'] = request.user.username
    return render(request, "task.html", context)


@login_required
def pool_edit_annotations(request, pool_id):
    context = base_context()
    pool = get_object_or_404(InstancePool, pk=pool_id)
    context['pool'] = pool
    instances = []
    InstanceTuple = namedtuple('InstanceTuple',
                               ['text', 'id', 'info', 'annotation', 'search_link'])
    for instance in pool.instances.all():
        try:
            annotation = instance.annotation_set.get(user=request.user)
            annotation_value = annotation.value
        except Annotation.DoesNotExist:
            annotation_value = ''
        instances.append(InstanceTuple(instance.text,
                                       instance.id,
                                       instance.info,
                                       annotation_value,
                                       get_search_link(instance)))
    instances.sort(key=lambda x: x.annotation, reverse=True)
    context['instances'] = instances
    add_url_to_context(context, 'annotate_instance',
                       reverse('annotate-ajax-annotate-instance'))
    return render(request, "pool.html", context)


@login_required
def pool_unannotated(request, pool_id):
    context = base_context()
    pool = get_object_or_404(InstancePool, pk=pool_id)
    context['pool'] = pool
    instances = []
    InstanceTuple = namedtuple('InstanceTuple',
                               ['text', 'id', 'info', 'annotation', 'search_link'])
    for instance in pool.instances.all():
        if instance.annotation_set.count() > 0:
            continue
        instances.append(InstanceTuple(instance.text,
                                       instance.id,
                                       instance.info,
                                       '',
                                       get_search_link(instance)))
    random.shuffle(instances)
    context['instances'] = instances
    add_url_to_context(context, 'annotate_instance',
                       reverse('annotate-ajax-annotate-instance'))
    return render(request, "pool.html", context)


@login_required
def get_random_task(request):
    tasks = []
    annotated_instances = set(
            Annotation.objects.values_list('instance_id', flat=True))
    pool_instances = defaultdict(list)
    for i in InstancePool.instances.through.objects.all():
        pool_instances[i.instancepool_id].append(i.instance_id)
    for task in Task.objects.filter(assignedTo__isnull=True):
        instances = set()
        annotated = set()
        selected = False
        for pool in task.instancepool_set.all():
            if not pool.selected: continue
            selected = True
            for instance in pool_instances[pool.id]:
                instances.add(instance)
                if instance in annotated_instances:
                    annotated.add(instance)
        if not selected: continue
        if len(instances.difference(annotated)) > 0:
            tasks.append(task)
    if len(tasks) == 0:
        return redirect('annotate-home')
    random.shuffle(tasks)
    task = tasks[0]
    task.assignedTo = request.user
    task.save()
    return redirect('annotate-task', task_id=task.id)


def pool_view_all_annotations(request, pool_id):
    context = base_context()
    pool = get_object_or_404(InstancePool, pk=pool_id)
    context['pool'] = pool
    instances = []
    InstanceTuple = namedtuple('InstanceTuple',
                               ['text', 'id', 'info', 'annotations', 'conflict', 'search_link'])
    AnnotationTuple = namedtuple('AnnotationTuple', ['user', 'value'])
    for instance in pool.instances.all():
        annotations = []
        for annotation in instance.annotation_set.all():
            annotations.append(AnnotationTuple(annotation.user.username,
                                               annotation.value))
        distinct_annotations = len(set([x.value for x in annotations]))
        conflict = False
        if distinct_annotations > 1:
            conflict = True
        instances.append(InstanceTuple(instance.text,
                                       instance.id,
                                       instance.info,
                                       annotations,
                                       conflict,
                                       get_search_link(instance)))
    context['instances'] = instances
    return render(request, "view_pool.html", context)


def pool_results(request, pool_id):
    context = base_context()
    pool = get_object_or_404(InstancePool, pk=pool_id)
    context['pool'] = pool
    instance_ids = pool.instances.values_list('id', flat=True)
    annotations_list = defaultdict(set)
    for annotation in Annotation.objects.filter(instance_id__in=instance_ids):
        annotations_list[annotation.instance].add(annotation.value)
    annotations = reconcile_annotations(annotations_list)
    MethodTuple = namedtuple('MethodTuple',
                             ['name', 'metrics', 'display_metrics'])
    methods = []
    context['total_instances'] = len(instance_ids)
    context['conflicting_annotations'] = len(annotations_list) - len(annotations)
    context['annotated_instances'] = len(annotations)
    context['annotated_correct'] = len([x for x in annotations if
                                        annotations[x] == 'correct'])
    context['annotated_maybe'] = len([x for x in annotations if
                                      annotations[x] == 'maybe'])
    context['metrics'] = get_display_metrics()
    for method in Method.objects.all():
        predictions = []
        for prediction in method.prediction_set.filter(task=pool.task):
            if prediction.instance in annotations:
                predictions.append(prediction.instance)
        metrics = get_metrics_from_predictions(predictions, annotations)
        display_metrics = get_values_in_order(metrics, context['metrics'])
        methods.append(MethodTuple(method.name, metrics, display_metrics))
    context['precision_recall_data'] = \
            get_precision_recall_data(methods, context['annotated_instances'])
    context['methods'] = methods
    return render(request, "pool_results.html", context)


@login_required
def annotate(request):
    instance_id = request.GET['instance_id']
    value = request.GET['value']
    instance = get_object_or_404(Instance, pk=instance_id)
    task = instance.task
    if not task.assignedTo:
        task.assignedTo = request.user
        task.save()
    try:
        annotation = Annotation.objects.get(instance=instance,
                                            user=request.user)
        annotation.value = value
    except Annotation.DoesNotExist:
        annotation = Annotation(instance=instance,
                                user=request.user,
                                value=value)
    annotation.save()
    return HttpResponse(value)


def reconcile_annotations(annotations_list):
    annotations = defaultdict(str)
    for instance, values in annotations_list.iteritems():
        if len(values) == 1:
            annotations[instance] = list(values)[0]
        # TODO(matt): try to figure out some way to reconcile these, instead of
        # just dropping conflicting annotations.
    return annotations


def get_metrics_from_predictions(predictions, annotations):
    metrics = {}
    correct = 0
    maybe_correct = 0
    predicted = 0
    total_precision = 0.0
    total_maybe_precision = 0.0
    first_correct_rank = -1
    prec_rec_list = []
    maybe_prec_rec_list = []
    for rank, prediction in enumerate(predictions):
        predicted += 1
        if annotations[prediction] == 'correct':
            if first_correct_rank == -1:
                first_correct_rank = rank + 1
            correct += 1
            maybe_correct += 1
        elif annotations[prediction] == 'maybe':
            maybe_correct += 1
        precision = float(correct) / predicted
        prec_rec_list.append(precision)
        total_precision += precision
        maybe_precision = float(maybe_correct) / predicted
        total_maybe_precision += maybe_precision
        maybe_prec_rec_list.append(maybe_precision)
    metrics['Predicted'] = predicted
    metrics['Correct'] = correct
    metrics['Maybe Correct'] = maybe_correct
    metrics['AP'] = total_maybe_precision / len(annotations)
    metrics['RR'] = 1.0 / first_correct_rank
    metrics['PR curve data'] = maybe_prec_rec_list
    return metrics


metrics_order = defaultdict(lambda: 1000)
metrics_order['AP'] = 1
metrics_order['RR'] = 2
metrics_order['Predicted'] = 3
metrics_order['Correct'] = 4
metrics_order['Maybe Correct'] = 5

def get_display_metrics():
    metrics = metrics_order.keys()
    metrics.sort(key=lambda x: metrics_order[x])
    return metrics


def get_values_in_order(metrics, display_metrics):
    return [metrics[x] for x in display_metrics]


def get_precision_recall_data(methods, num_annotations):
    results = []
    headers = ['Recall']
    for method in methods:
        headers.append(method.name.encode('ascii'))
    results.append(headers)
    for i in range(num_annotations):
        line = [float(i+1) / num_annotations]
        for method in methods:
            try:
                line.append(method.metrics['PR curve data'][i])
            except IndexError:
                line.append(0)
        results.append(line)
    return results


def get_search_link(instance):
    return get_freebase_link(instance)
    #return get_google_search_link(instance)


def get_freebase_link(instance):
    return 'http://freebase.com' + instance.text


def get_google_search_link(instance):
    text = instance.text
    if '(' in text:
        args = text.split('(')[1].split(')')[0].split(', ')
        #relation = text.split('(')[0]
        text = args[0] + ' ' + args[1]
    return 'http://google.com/search?q=' + text.replace('_', ' ').replace(' ', '+')


def add_url_to_context(context, varname, link):
    Url = namedtuple('Url', ['varname', 'link'])
    context['urls'].append(Url(varname, link))


def base_context():
    context = {}
    context['urls'] = []
    return context
