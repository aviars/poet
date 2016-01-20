#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
poet
FILE: models
Created: 1/12/16 11:00 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from .choices import POET_BUNDLE_REFERENCE

@python_2_unicode_compatible
class PoetMember(models.Model):
    organization        = models.CharField(max_length=256, unique=True,
                                           db_index=True)
    # active_account      = models.BooleanField(default=True, verbose_name="Active Account")
    hostname            = models.CharField(max_length=256, unique=False)
    bundle_reference    = models.CharField(max_length=40,
                                           choices=POET_BUNDLE_REFERENCE,
                                           default="",
                                           blank=True,
                                           unique=False)
    owner_email         = models.EmailField(max_length=256,
                                            blank=False,
                                            unique=False)
    secret_key          = models.TextField(max_length=5120, unique=False)


    # Python2 uses __unicode__(self):
    def __str__(self):
        return self.organization


    def active(self):
        return self.active
