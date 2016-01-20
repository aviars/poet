#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
poet
FILE: utils
Created: 1/14/16 3:35 PM

functions used by settings.py to read contents from local.ini settings file

"""
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
