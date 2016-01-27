#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
poet
FILE: settings.local
Purpose: local configuration
Created: 1/12/16 11:47 AM

Credit to Revolution System for best practice recommendations
http://www.revsys.com/blog/2014/nov/21/recommended-django-project-layout/

"""
__author__ = 'Mark Scrimshire:@ekivemark'

from .base import *

ENVIRONMENT_MODE = "local"
# Set OS Environment as follows:
# export DJANGO_SETTINGS_MODULE=poet.settings.local


import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLICATION_ROOT = BASE_DIR

from configparser import RawConfigParser

from ..utils import  str2bool, str2int

PARSE_INI = RawConfigParser()
# IMPORTANT: Exclude the config file (local.ini) from git
CONFIG_FILE = '../local.ini'
# Read the config file
PARSE_INI.read_file(open(os.path.join(APPLICATION_ROOT, CONFIG_FILE)))
# Then use PARSE_INI.get(SECTION, VARIABLE) to read in value
# Value is in string format
# Use util functions to convert strings to boolean or Integer

# Set a fake SECRET_KEY then overwrite with value from local.ini file
SECRET_KEY = 'FAKE_VALUE_REAL_VALUE_SET_FROM_..LOCAL.INI'
SECRET_KEY = PARSE_INI.get('global', 'secret_key')

DEBUG=True
#TEMPLATE_DEBUG=True
# Deprecated in Django 1.8. Add to TEMPLATES Dictionary

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Put strings here, like "/home/html/django_templates" or
            # "C:/www/django/templates".
            # Always use forward slashes, even on Windows.
            # Don't forget to use absolute paths, not relative paths.
            # This should always be the last in the list because it is our default.
            os.path.join(BASE_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                #'django_settings_export.settings_export',
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.debug',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'debug': True,
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db/local.sqlite3'),
    }
}

ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'sitestatic'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATIC_URL = '/static/'

# CORSHEADERS Configuration
# Set ALLOW_ALL to True for testing only
CORS_ORIGIN_ALLOW_ALL = True

# End of CORSHEADERS Section


print("=============================================================")
print("Application: ", APPLICATION_TITLE)
print("POET Environemnt Settings")
print("Environment:", ENVIRONMENT_MODE)
print("BASE_DIR:", BASE_DIR)
print("=============================================================")
