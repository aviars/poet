#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
poet
FILE: member
Created: 1/19/16 11:17 AM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  )


from ..models import PoetMember

class StaffRequiredMixin(object):
    """
    View mixin which requires that the authenticated user is a staff member
    (i.e. `is_staff` is True).
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(
                request,
                'You do not have the permission required to perform the '
                'requested operation.')
            return redirect(settings.LOGIN_URL)
        return super(StaffRequiredMixin, self).dispatch(request,
            *args, **kwargs)


class MemberList(ListView):

    model = PoetMember

    context_object_name = 'poetmembers'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MemberList, self).dispatch(*args, **kwargs)


class MemberCreate(StaffRequiredMixin, CreateView):

    model = PoetMember

    slug_field = 'organization'

    fields = ['bundle_reference',
              'organization',
              'hostname',
              'owner_email',
              'secret_key',
              # 'active_account',
              ]

    success_url = reverse_lazy('member_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MemberCreate, self).dispatch(*args, **kwargs)


class MemberView(DetailView):

    model = PoetMember

    slug_field = 'id'

    context_object_name = 'member'
    fields = ['bundle_reference',
              'organization',
              'hostname',
              'owner_email',
              'secret_key',
              # 'active_account',
              ]

    success_url = reverse_lazy('member_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MemberView, self).dispatch(*args, **kwargs)


class MemberUpdateView(StaffRequiredMixin, UpdateView):

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

    success_url = reverse_lazy('member_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MemberUpdateView, self).dispatch(*args, **kwargs)


class MemberDeleteView(StaffRequiredMixin, DeleteView):

    model = PoetMember

    success_url = reverse_lazy('member_list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MemberDeleteView, self).dispatch(*args, **kwargs)

