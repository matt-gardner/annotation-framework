#!/usr/bin/env python

import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'framework.settings'
sys.path.append('.')
sys.path.append('../')

import django
django.setup()
from annotate.models import Task

predicates_to_annotate = set([
        'specializations:academicfield',
        'specializations:animal',
        'specializations:bodypart',
        'specializations:bakedgood',
        'specializations:disease',
        'specializations:fruit',
        'specializations:officeitem',
        'specializations:planet',
        'specializations:sport',
        'specializations:sportsteam',
        'specializations:sportsleague',
        'specializations:athlete',
        'specializations:emotion',
        'specializations:musicinstrument',
        'specializations:visualartform',
        'specializations:visualartmovement',
        'specializations:wine',
        'specializations:militaryconflict',
        'actorstarredinmovie',
        'airportincity',
        'animaleatfood',
        'athleteplaysforteam',
        'athleteplayssport',
        'bookwriter',
        'ceoof',
        'citycapitalofcountry',
        'citylocatedincountry',
        'teamplayssport',
        'teamhomestadium',
        'musicianplaysinstrument',
        'itemfoundinroom',
        ])

if __name__ == '__main__':
    for predicate in predicates_to_annotate:
        try:
            task = Task.objects.get(name=predicate)
            for pool in task.instancepool_set.all():
                if '(old)' in pool.name:
                    pool.selected = False
                else:
                    pool.selected = True
                pool.save()
        except Task.DoesNotExist:
            print 'Task not found:', predicate
