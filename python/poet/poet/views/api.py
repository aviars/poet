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

import json

from collections import OrderedDict
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import PoetMember, EntityCheckLog
from ..utils import (body_decode2json,
                     kickout_400,
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

        # decode the json from request.body
        j = body_decode2json(request)
        # We received Json in the POST. Now we process it.

        requested_by = pull_data(j, 'requested_by')
        bundle_ref   = pull_data(j, 'bundle')
        domain       = pull_data(j, 'domain')
        owner        = pull_data(j, 'owner')
        secret       = pull_data(j, 'shared_secret')
        tx           = "EC"

        joined = ""
        success = False
        org = ""
        try:
            member = PoetMember.objects.get(bundle_reference=bundle_ref,
                                            owner_email=owner,
                                            hostname=domain
                                            )
            if member.active_account:
                if member.secret_key == secret:
                    success = True
                    joined = member.created.isoformat()
                else:
                    success = False
            else:
                success = False
            org = member.organization

        except PoetMember.DoesNotExist:
            success = False
            joined = ""
            org = ""

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
        log.save()

        # Get the GUID from log.reference and the timestamp
        tx_ref = log.reference
        tx_time = log.timestamp.isoformat()

        if not success:
            return kickout_404("Not Found",)

        result = OrderedDict()
        result['validation_timestamp'] = tx_time
        result['joined_bundle'] = joined
        result['transaction_reference'] = tx_ref
        result['success'] = success

        return HttpResponse(json.dumps(result,
                                       indent=4),
                            content_type="application/json")

    else:
        # return a 404
        reason = request.method +": not accepted. POST required."
        return kickout_404(reason,)


@csrf_exempt
def StillValid(request):
    """
    StillValid will receive a json payload via a POST call
    unpack the payload and use list of entities to check if entity is still trusted.
    return json payload with Trusted_Entity and NotTrusted_Entity that lists trusted and
    no longer trusted entities.

    :param request:
    :return:

{
 "entities": [
              {"name": organization_name or id,
               "bundle": bundle_id,
               “domain”: domain,
               “owner”: owner_email,
              },
              ]
}

    Unpack each dictionary and check for active_account = True

    If active_account

    """

    tx = "EV"
    if request.method == 'POST':
        # Get the payload

        # decode the json from request.body
        j = body_decode2json(request)
        # We received Json in the POST. Now we process it.

        entities = pull_data(j, 'entities')

        validated = list()
        failed    = list()

        then = datetime.now()
        validity_check_start = then.isoformat()
        for entity in entities:
            org = entity['name']
            if 'bundle' in entity and 'owner' in entity and 'domain' in entity:
                try:
                    PoetMember.objects.get(bundle_reference=entity['bundle'],
                                           owner_email=entity['owner'],
                                           hostname=entity['domain'])
                    validated.append(org)
                except PoetMember.DoesNotExist:
                    failed.append(org)
            else:
                failed.append(org)

        now =  datetime.now()
        validity_check_end = now.isoformat()

        result = OrderedDict()
        result['begin_check']= validity_check_start
        result['validated'] = validated
        result['failed'] = failed
        result['end_check'] = validity_check_end

        return HttpResponse(json.dumps(result, indent=4),
                            content_type="application/json")

    else:
        # return a 404
        reason = request.method +": not accepted. POST required."
        return kickout_404(reason,)


