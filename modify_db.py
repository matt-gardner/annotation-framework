#!/usr/bin/env python

import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'framework.settings'

import django
django.setup()
from annotate.models import *
from django.contrib.auth.models import User

# vim: et sw=4 sts=4
