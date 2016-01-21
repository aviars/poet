#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
poet
FILE: api
Created: 1/21/16 12:44 AM


These API calls will be protected by OAuth2

"""
__author__ = 'Mark Scrimshire:@ekivemark'
import datetime
import json

from collections import OrderedDict

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import PoetMember, EntityCheckLog
from ..utils import (kickout_400,
                     kickout_404,
                     pull_data)

@csrf_exempt
def EntityCheck(request):
    """
    EntityCheck will receive a json payload via a POST call
    unpack the payload and look up POET Member using supplied information

{
 “requested_by”: requester_email,
 “bundle”: bundle_id,
 “domain”: domain,
 “owner”: owner_email,
 “shared_secret”: shared_secret,
}

    if complete match return 200 with date created


    Record the request and result in EntityCheckLog
{
  "validation_timestamp": "YYYYMMDD.HHMM",
  "joined_bundle": "YYYYMMDD.HHMM",
  "transaction_reference": guid,
  "success": "True"
}
    if fail to match return 404

    """
    if request.method == "POST":
        # Get the payload

        try:
            j =json.loads(request.body.decode('utf-8'), object_pairs_hook=OrderedDict)
            if type(j) !=  type({}):
                kickout_400("The request body did not contain a JSON object i.e. {}.")
        except:
            if settings.DEBUG:
                    print("Failed with:", request.body)
            return kickout_400("The request body did not contain valid JSON.",)
        # We received Json in the PUT. Now we process it.

        requested_by = pull_data(j, 'requested_by')
        bundle_ref   = pull_data(j, 'bundle')
        domain       = pull_data(j, 'domain')
        owner        = pull_data(j, 'owner')
        secret       = pull_data(j, 'shared_secret')
        tx           = "EC"

        try:
            member = PoetMember.objects.get(bundle_reference=bundle_ref,
                                            owner_email=owner,
                                            hostname=domain,
                                            secret_key=secret)
            if member.active_account:
                if member.secret_key == secret:
                    success = True
                    joined = datetime.datetime.strftime(member.created,
                                                        '%Y%m%d.%H%M%S%f')
                    if settings.DEBUG:
                        print("We got a match!")
                else:
                    success = False
                    joined = ""
            else:
                success = False
                joined = ""
            org = member.organization

        except PoetMember.DoesNotExist:
            if settings.DEBUG:
                print("We didn't match!")
            success = False
            joined = ""
            org = ""

        if settings.DEBUG:
            print("About to record the Transaction")
        # Write a Transaction log and get a Guid and Timestamp

        log = EntityCheckLog(requested_by=requested_by,
                             organization=org,
                             bundle=bundle_ref,
                             domain=domain,
                             owner=owner,
                             tx=tx,
                             success=success,
                             user=request.user,
                             )
        if settings.DEBUG:
            print("log instance created:", log)
            print("Organization:", org)
            print('requested_by:', requested_by)

        log.save()

        if settings.DEBUG:
            print("We wrote a log entry")
        # Get the GUID from log.reference and the timestamp
        tx_ref = log.reference
        tx_time = datetime.datetime.strftime(log.timestamp, '%Y%m%d.%H%M%S%f')
        if settings.DEBUG:
            print("Timestamp:", log.timestamp)
            print("Text Time:", tx_time)

        if not success:
            return kickout_404("Not Found",)

        result = OrderedDict()
        result['validation_timestamp'] = tx_time
        result['joined_bundle'] = joined
        result['transaction_reference'] = tx_ref
        if success:
            result['success'] = "True"
        else:
            result['success'] = "False"
        if settings.DEBUG:
            print("We prepared the response")
            print(result)
        return HttpResponse(json.dumps(result,
                                       indent=4),
                            content_type="application/json")

    else:
        # return a 404
        reason = request.method +": not accepted. POST required."
        return kickout_404(reason,)


def StillValid(request):
    """
    StillValid will receive a json payload via a PUT call
    unpack the payload and use list of entities to check if entity is still trusted.
    return json payload with Trusted_Entity and NotTrusted_Entity that lists trusted and
    no longer trusted entities.

    :param request:
    :return:


    """
    if request.method == 'POST':

        od = OrderedDict()
        od['request_method']= request.method
        od['interaction_type'] = "EntityCheck"
        od['json_received'] = j
        od['note'] = "Perform an HTTP POST to this URL with the JSON resource as the request body."

        return HttpResponse(json.dumps(od, indent=4),
                            content_type="application/json")

    else:
        # return a 404
        reason = request.method +": not accepted. POST required."
        return kickout_404(reason,)


