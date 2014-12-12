#!/usr/bin/env python

import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'framework.settings'
sys.path.append('.')
sys.path.append('../')

import django
django.setup()
from django.contrib.auth.models import User

if __name__ == '__main__':
    for user in sys.argv[1:]:
        u = User(username = user)
        u.set_password(user)
        u.save()
