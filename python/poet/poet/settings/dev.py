#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
poet
FILE: settings.dev
Purpose: Beta install in AWS - dev.bbonfhir.com
Created: 1/12/16 11:47 AM

Credit to Revolution System for best practice recommendations
http://www.revsys.com/blog/2014/nov/21/recommended-django-project-layout/

"""
__author__ = 'Mark Scrimshire:@ekivemark'

from base import *

DEBUG=True
TEMPLATE_DEBUG=True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db/dev.sqlite3'),
    }
}