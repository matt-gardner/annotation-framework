#!/usr/bin/env python

import os

from collections import defaultdict

def main():
    annotations = read_annotations('data/annotations.tsv')
    predictions = defaultdict(lambda: defaultdict(list))
    for file in os.listdir('data/filtered'):
        read_predictions('data/filtered/' + file, predictions)
    final_metrics_list = defaultdict(lambda: defaultdict(list))
    methods = []
    for method in predictions:
        methods.append(method)
        for task in predictions[method]:
            prediction_list = predictions[method][task]
            prediction_list.sort(key=lambda x: x[1])
            prediction_list = [x[0] for x in prediction_list]
            metrics = get_metrics_from_predictions(prediction_list,
                                                   annotations[task])
            final_metrics_list[method]['MAP'].append(metrics['AP'])
            final_metrics_list[method]['MRR'].append(metrics['RR'])
            final_metrics_list[method]['MeanP@10'].append(metrics['P@10'])
            final_metrics_list[method]['MeanP@25'].append(metrics['P@25'])
    final_metrics = defaultdict(dict)
    for method, metrics in final_metrics_list.iteritems():
        map = sum(metrics['MAP']) / len(metrics['MAP'])
        mrr = sum(metrics['MRR']) / len(metrics['MRR'])
        mean_p_at_10 = sum(metrics['MeanP@10']) / len(metrics['MeanP@10'])
        mean_p_at_25 = sum(metrics['MeanP@25']) / len(metrics['MeanP@25'])
        final_metrics[method]['MAP'] = map
        final_metrics[method]['MRR'] = mrr
        final_metrics[method]['MeanP@10'] = mean_p_at_10
        final_metrics[method]['MeanP@25'] = mean_p_at_25
    methods.sort(key=lambda x: final_metrics[x]['MAP'], reverse=True)
    print '%-10s' % 'Iteration',
    print ' %6s ' % 'MAP',
    print ' %6s ' % 'MRR',
    print ' %10s ' % 'MeanP@10',
    print ' %10s ' % 'MeanP@25'
    for method in methods:
        print '%-10s' % method,
        print ' %.4f ' % final_metrics[method]['MAP'],
        print ' %.4f ' % final_metrics[method]['MRR'],
        print '     %.4f ' % final_metrics[method]['MeanP@10'],
        print '     %.4f ' % final_metrics[method]['MeanP@25']


def read_annotations(filename):
    annotations = defaultdict(lambda: defaultdict(set))
    for line in open(filename):
        fields = line.strip().split('\t')
        task = fields[0]
        instance = fields[1]
        value = fields[3]
        annotations[task][instance].add(value)
    return reconcile_annotations(annotations)


def reconcile_annotations(annotations_list):
    annotations = defaultdict(lambda: defaultdict(str))
    for task in annotations_list:
        for instance, values in annotations_list[task].iteritems():
            if len(values) == 1:
                annotations[task][instance] = list(values)[0]
            # TODO(matt): try to figure out some way to reconcile these, instead of
            # just dropping conflicting annotations.
    return annotations


def read_predictions(filename, predictions):
    for line in open(filename):
        fields = line.strip().split('\t')
        task = fields[0]
        instance = fields[3]
        rank = int(fields[2])
        method = fields[1]
        predictions[method][task].append((instance, rank))


def get_metrics_from_predictions(predictions, annotations):
    metrics = {}
    correct = 0
    maybe_correct = 0
    predicted = 0
    total_precision = 0.0
    total_maybe_precision = 0.0
    first_correct_rank = -1
    ks = [10, 25]
    correct_at_k = defaultdict(int)
    seen_at_k = defaultdict(int)
    for rank, prediction in enumerate(predictions):
        if prediction not in annotations:
            #if rank < k: print 'No annotation for item less than rank k!'
            continue
        predicted += 1
        for k in ks:
            if rank < k:
                seen_at_k[k] += 1
        if annotations[prediction] == 'correct':
            for k in ks:
                if rank < k:
                    correct_at_k[k] += 1
            if first_correct_rank == -1:
                first_correct_rank = rank + 1
            correct += 1
            maybe_correct += 1
        elif annotations[prediction] == 'maybe':
            maybe_correct += 1
        precision = float(correct) / predicted
        total_precision += precision
        maybe_precision = float(maybe_correct) / predicted
        total_maybe_precision += maybe_precision
    metrics['Predicted'] = predicted
    metrics['Correct'] = correct
    metrics['Maybe Correct'] = maybe_correct
    metrics['AP'] = total_maybe_precision / len(annotations)
    metrics['RR'] = 1.0 / first_correct_rank if first_correct_rank != -1 else 0
    for k in ks:
        metrics['P@%d' % k] = float(correct_at_k[k]) / seen_at_k[k]
    return metrics


if __name__ == '__main__':
    main()
