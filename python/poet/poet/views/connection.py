#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
poet
FILE: connection
Created: 1/25/16 5:22 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
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


from ..models import Connections


class ConnectionsList(ListView):
    """
    Display Organizations connected to a user account
    """

    model = Connections

    slug_field = "pk"

    context_object_name = 'connections'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ConnectionsList, self).dispatch(*args, **kwargs)


    # def get_context_data(self, *args, **kwargs):
    #     context = super(ConnectionsList, self).get_context_data(**kwargs)
    #     self.pk = self.kwargs.get('pk')
    #     print("Connections Key is ", self.pk)
    #     print("KWArgs:", self.kwargs)
    #
    #     if self.pk != None:
    #         print("we got a key", self.pk)
    #         context['connections'] = Connections.objects.get(user=self.pk)
    #         return context
    #     if self.request.user.is_staff:
    #         context['connections'] = Connections.objects.all()
    #     else:
    #         context['connections'] = Connections.objects.filter(user=self.request.user.id)
    #
    #     return context


    def get_queryset(self):
        self.pk = self.kwargs.get('pk')
        print("Connections Key =", self.pk)
        if self.pk != None:
            return Connections.objects.filter(pk=self.pk)
        if self.request.user.is_staff:
            return Connections.objects.all()
        else:
            return Connections.objects.filter(user=self.request.user)



class UserList(ListView):
    """
    Display Users connected to a user account
    """

    model = settings.AUTH_USER_MODEL

    context_object_name = 'users'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        User = get_user_model()
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(username=self.request.user.username)

