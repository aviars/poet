#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
poet
FILE: utils
Created: 1/14/16 3:35 PM

functions used by settings.py to read contents from local.ini settings file

"""
from collections import OrderedDict
from django.conf import settings
from django.http import HttpResponse
import json

__author__ = 'Mark Scrimshire:@ekivemark'


def str2bool(inp):
    output = False
    if inp.upper() == "TRUE":
        output = True
    elif inp.upper() == "FALSE":
        output = False

    return output


def str2int(inp):
    output = 0 + int(inp)

    return output


def body_decode2json(request):
    """
    Get the json input from the request.body
    :param request:
    :return: j
    """

    try:
        j =json.loads(request.body.decode('utf-8'), object_pairs_hook=OrderedDict)
        if type(j) !=  type({}):
            kickout_400("The request body did not contain a JSON object i.e. {}.")
        if settings.DEBUG:
            print("J contains:", j)
        return j
    except:
        return kickout_400("The request body did not contain valid JSON.",)




def pull_data(payload, key):
    """
    lookup key in the json payload and return the value
    """
    if key in payload:
        return payload[key]
    else:
        return ""


def kickout_400(reason, status_code=400):
    response= OrderedDict()
    response["code"] = status_code
    response["errors"] = [reason,]
    return HttpResponse(json.dumps(response, indent = 4),
                        status=status_code,
                        content_type="application/json")


def kickout_401(reason, status_code=401):
    response= OrderedDict()
    response["code"] = status_code
    response["errors"] = [reason,]
    return HttpResponse(json.dumps(response, indent = 4),
                        status=status_code,
                        content_type="application/json")


def kickout_403(reason, status_code=403):
    response= OrderedDict()
    response["code"] = status_code
    response["errors"] = [reason,]
    return HttpResponse(json.dumps(response, indent = 4),
                        status=status_code,
                        content_type="application/json")


def kickout_404(reason, status_code=404):
    response= OrderedDict()
    response["code"] = status_code
    response["errors"] = [reason,]
    return HttpResponse(json.dumps(response, indent = 4),
                        status=status_code,
                        content_type="application/json")


def kickout_500(reason, status_code=500):
    response= OrderedDict()
    response["code"] = status_code
    response["errors"] = [reason,]
    return HttpResponse(json.dumps(response, indent = 4),
                        status=status_code,
                        content_type="application/json")