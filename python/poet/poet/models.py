#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
poet
FILE: models
Created: 1/12/16 11:00 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from uuid import uuid4

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from .choices import (POET_BUNDLE_REFERENCE,
                      POET_TRANSACTION_TYPE)

@python_2_unicode_compatible
class PoetMember(models.Model):
    organization        = models.CharField(max_length=256, unique=True,
                                           db_index=True)
    active_account      = models.BooleanField(default=True, verbose_name="Active Account")
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
    created             = models.DateTimeField(editable=False)
    modified            = models.DateTimeField()


    # Python2 uses __unicode__(self):
    def __str__(self):
        return self.organization


    def active(self):
        return self.active_account


    def get_absolute_url(self):
        return reverse('poetmember_detail', kwargs={'pk': self.pk})


    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(PoetMember, self).save(*args, **kwargs)


@python_2_unicode_compatible
class EntityCheckLog(models.Model):
    reference           = models.CharField(max_length=40,
                                           blank=False,
                                           unique=True,
                                           editable=False,
                                           db_index=True)
    requested_by        = models.EmailField(max_length=256,
                                            blank=False,
                                            unique=False)
    organization        = models.CharField(max_length=256,
                                           unique=False,
                                           db_index=True)
    bundle              = models.CharField(max_length=40,
                                           blank=True,
                                           unique=False)
    domain              = models.CharField(max_length=256,
                                           unique=False)
    owner               = models.EmailField(max_length=256,
                                            blank=False,
                                            unique=False)
    success             = models.BooleanField(default=False)
    timestamp           = models.DateTimeField(editable=False)
    tx                  = models.CharField(max_length=4,
                                           choices=POET_TRANSACTION_TYPE,
                                           default="----",
                                           blank=False)
    user                = models.ForeignKey(settings.AUTH_USER_MODEL)


    # Python2 uses __unicode__(self):
    def __str__(self):
        LogEntry = self.requested_by + "(" + str(self.timestamp) + ")"
        return LogEntry


    def get_absolute_url(self):
        return reverse('entitychecklog_detail', kwargs={'pk': self.pk})


    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.timestamp = timezone.now()
            # Assign a GUID with the save
            uid = str(uuid4().urn)[9:]
            # uid4.urn returns string:
            # eg. 'urn:uuid:aec9931c-101b-4803-8666-f047c9159c0c'
            # str()[9:] strips leading "urn:uuid:"
            self.reference = uid
        return super(EntityCheckLog, self).save(*args, **kwargs)

