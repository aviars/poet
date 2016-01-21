#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
poet
FILE: models
Created: 1/12/16 11:00 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from .choices import POET_BUNDLE_REFERENCE

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