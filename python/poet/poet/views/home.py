from collections import OrderedDict
from django.http import HttpResponse

import json

def home(request):
    """Welcome to POET - Pre-OAuth Entity Trust API"""
    # Example client use in curl:
    # curl http://127.0.0.1:8000/poet/hello

    od = OrderedDict()
    od['note'] = "Hello.  Welcome to the POET Server. This is an example API to verify the " \
                 "identity of an organization in a Community of Trust. Call the Trust API " \
                 "to get a response."
    return HttpResponse(json.dumps(od, indent=4),
                        content_type="application/json")