# Pre OAuth Entity Trust API (POET) 
(Previously known as:OAuth Trust Whitelist API)

## Document Information:

### Author: 
Mark Scrimshire (mark@ekivemark.com)

Google Drive Link for comments: https://docs.google.com/document/d/1-LHUL-2iy8Y4duZGN_7Z7mCKjSMBCdo9rdOWgurQ4Zk/edit?usp=sharing

### Version: 1.1

# Background

The Centers for Medicare and Medicaid Services (CMS) is building a next generation BlueButton service. This will be a REST API that will present HL7 FHIR structured data resources.

The service will enable Medicare beneficiaries to connect their data to the applications, services and research programs they trust.

CMS needs to be able to perform some basic validation of the third party application before issuing an application key. 

The purpose of this specification is to create a POET API that reaches out to direct messaging trust bundle providers to confirm that an entity is a valid member of a legitimate trust bundle.

The POET API will validate the data provided and return either a 404 Not found or a 200 Ok with a datetime entry that identify when the certificate for the entity expires.

# Security

The POET API is intended for organizations, such as CMS, that want to validate requests for third party application access against existing healthcare industry validation services such as DirectTrust or NATE (National Association for Trusted Exchange).

The API will use OAuth2 to control authorization and the API will be offered over a secure HTTPS/SSL connection.

# API Payload

The API call will be a POST with a json payload to /api/entitycheck/ on the POET Server.

The call to the POET API endpoint will be a POSTT request with a JSON payload as follows :

    {
     “requested_by”: requester_email,
     “bundle”: bundle_id,
     “domain”: domain,
     “owner”: owner_email,
     “shared_secret”: shared_secret,
    }

requested_by: this is the email address of the person making the application for, the originating site. This is typically a developers really administrator in the third party application development organization.

bundle_id: this is an id to allow the POET API to recognize which trust bundle the entity is registered in. This allows a trust organization to accommodate multiple trust bundles.

domain: the is the domain that is registered in the trust bundle for the entity.

owner: this is the email of the organization representative that controls the entity account within the trust bundle. This is typically the email address of the person who applied for their organization to join the given trust bundle.

shared_secret: this is a key that is maintained for the entity outside of the trust bundle certificate. It is a key that is known only to the administrative owner of an entity in the trust bundle.

# API Actions

## Entity Check (/api/entitycheck/)

The POET API will analyze the content of the JSON payload and attempt a match to an entity in the trust bundle identified by the submitter. 

If the submitter provides incorrect information the API will return a 404 “Not found” http response.

    {
    "code": 404,
    "errors": [
        "Not Found"
    ]
    }

If all of the fields are supplied correctly the API will identify the trust certificate for the entity and return the expiry date in a JSON response as follows :

    {
    "validation_timestamp": "2016-01-22T06:14:01.015919+00:00",
    "joined_bundle": "2016-01-20T23:02:28.421837+00:00",
    "transaction_reference": "284c9f59-4211-4a12-befe-b815b82a946d",
    "success": true
    }

### validation_timestamp

The date and time when the entity was validated by the POET Server. 
Time is in iso format.

### joined_bundle

The date and time when the entity was added to the Trust Bundle on the POET Server.
Time is in iso format.

### transaction_reference

A unique Transaction Id issued by the POET Server.

### success

An indicator to confirm a successful match for the entity on the POET Server.
A True or False value. The only value received should be True. Failed matches will return a 
404 message.

## Entity Still Valid (/api/entitystillvalid/)

The POET will analyze the content of the Json payload from the POST. The POET Server will
iterate through the list of entities and check for PoetMember.account_active = True.

The name is added to the validated list if account_active = True.
The name is added to the failed list is a record is not found or account_active = False.

The json payload is as follows:

    {
     "entities": [
       {"name": organization,
        "bundle": bundle_id,
        "domain": domain,
        "owner": owner_email},
       {"name": organization,
        "bundle": bundle_id,
        "domain": domain,
        "owner": owner_email}, ...
       ]
    }

The json payload returned is as follows:

    {
     "begin_check": "2016-01-22T01:17:10.566858",
     "validated": [
                   "Medyear"
                  ],
     "failed": [
                "Bad_one"
               ],
     "end_check": "2016-01-22T01:17:10.574513"
    }

## begin_check

The date and time the validation check starts in iso format

## validated

The list of organization names in text format that passed validation. The name is taken from
the entities["name"] field in the submitted json payload.

## failed

The list of organization names in text format that failed validation. The name is taken from
the entities["name"] field in the submitted json payload.

An organization can fail validation if:
- The PoetMember record has account_active = False
- A PoetMember record is not found for the combination of bundle, domain and owner_email submitted

## end_check

The date and time the validation check end in iso format
