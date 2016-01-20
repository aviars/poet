#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
poet
FILE: admin
Created: 1/20/16 12:15 AM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django import forms
from django.contrib import admin

from django.conf import settings

from .models import PoetMember

class PoetMemberAdmin(admin.ModelAdmin):
    """
    Admin form for PoetMember model
    """

    #form = PoetMemberForm

    list_display = ('organization', 'bundle_reference', 'owner_email')
    # readonly_fields = ('created', 'modified', 'author')
    exclude = ['active_account']

    def save_model(self, request, obj, form, change):
        """
        When creating a new object, set the creator field.
        """
        if settings.DEBUG:
            print("Saving model with ", request.user)
            print("mode=", change)
        if not change:
            obj.author = request.user

        obj.save()


admin.site.register(PoetMember, PoetMemberAdmin)
