#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
poet
FILE: setup.py
Created: 1/12/16 12:34 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))




setup(name='django-poet',
      version="0.0.0.1a",
      license='Apache',
      packages=['python.poet'],
      description="A POET API Server as a reusable Django application",
      long_description=README,
      author="Mark Scrimshire: @ekivemark",
      author_email="mark@ekivemark.com",
      url="https://github.com/ekivemark/poet",
      download_url="https://gitbub.com/ekivemark/poet/tarball/master",
      install_requires=[
        'django==1.8.7', 'django-oauth-toolkit',
        'django-cors-headers', 'jsonschema'],
      include_package_data=True,
      scripts=[],
      classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],




      )
