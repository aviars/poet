from ..models import PoetMember
from collections import OrderedDict
from django.http import HttpResponse

import json

def hello(request):
    """Hello POET"""
    # Example client use in curl:
    # curl http://127.0.0.1:8000/poet/hello

    od = OrderedDict()
    od['note'] = "Hello.  Welcome to the POET Server."
    return HttpResponse(json.dumps(od, indent=4),
                        content_type="application/json")