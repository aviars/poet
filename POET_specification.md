# Pre OAuth Entity Trust API (POET) 
(Previously known as:OAuth Trust Whitelist API)

## Document Information:

### Author: Mark Scrimshire (mark@ekivemark.com)

### Google Drive Link for comments: https://docs.google.com/document/d/1-LHUL-2iy8Y4duZGN_7Z7mCKjSMBCdo9rdOWgurQ4Zk/edit?usp=sharing

### Version: 1.1

# Background

The Centers for Medicare and Medicaid Services (CMS) is building a next generation BlueButton service. This will be a REST API that will present HL7 FHIR structured data resources.

The service will enable Medicare beneficiaries to connect their data to the applications, services and research programs they trust.

CMS needs to be able to perform some basic validation of the third party application before issuing an application key. 

The purpose of this specification is to create a whitelist API that reaches out to direct messaging trust bundle providers to confirm that an entity is a valid member of a legitimate trust bundle.

The whitelist API will validate the data provided and return either a 404 Not found or a 200 Ok with a datetime entry that identify when the certificate for the entity expires.

# Security

The whitelist API is intended for organizations, such as CMS, that want to validate requests for third party application access against existing healthcare industry validation services such as DirectTrust or NATE (National Association for Trusted Exchange).

The API will use OAuth2 to control authorization and the API will be offered over a secure HTTPS/SSL connection.

# API Payload

The call to the Whitelist API endpoint will be a PUT request with a JSON payload as follows:

{
“requested_by”: requester_email,
“bundle”: bundle_id,
“domain”: domain,
“owner”: owner_email,
“shared_secret”: shared_secret,
}

requested_by: this is the email address of the person making the application for, the originating site. This is typically a developers really administrator in the third party application development organization.

bundle_id: this is an id to allow the whitelist API to recognize which trust bundle the entity is registered in. This allows a trust organization to accommodate multiple trust bundles.

domain: the is the domain that is registered in the trust bundle for the entity.

owner: this is the email of the organization representative that controls the entity account within the trust bundle. This is typically the email address of the person who applied for their organization to join the given trust bundle.

shared_secret: this is a key that is maintained for the entity outside of the trust bundle certificate. It is a key that is known only to the administrative owner of an entity in the trust bundle.

# API Actions

The Whitelist API will assess the content of the JSON payload. 

If the submitter provides incorrect information the API will return a 404 “Not found” http response.

If all of the fields are supplied correctly the API will identify the trust certificate for the entity and return the expiry date in a JSON response as follows:

{
“expires”: “YYYYMMDD.HHMM”
}

