from collections import OrderedDict
from django.shortcuts import render_to_response
from django.template.response import RequestContext
import json

def home(request):
    """Welcome to POET - Pre-OAuth Entity Trust API"""
    # Example client use in curl:
    # curl http://127.0.0.1:8000/poet/home

    context = {}

    return render_to_response('index.html',
                              RequestContext(request, context, ))

