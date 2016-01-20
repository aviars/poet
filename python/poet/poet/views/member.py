#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
poet
FILE: member
Created: 1/19/16 11:17 AM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView)


from ..models import PoetMember


class MemberList(ListView):

    model = PoetMember

    context_object_name = 'poetmembers'

class MemberCreate(CreateView):

    model = PoetMember
    slug_field = 'organization'

    fields = ['bundle_reference',
              'organization',
              'hostname',
              'owner_email',
              'secret_key',
              # 'active_account',
              ]

class MemberView(DetailView):

    model = PoetMember

    slug_field = 'organization'

    context_object_name = 'member'
    fields = ['bundle_reference',
              'organization',
              'hostname',
              'owner_email',
              'secret_key',
              # 'active_account',
              ]
