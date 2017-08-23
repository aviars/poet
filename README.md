Pre-OAuth Entity Trust (POET) - DRAFT
======================================

POET was conceived as a means to represent third-party application endorsement for health care applications. POET’s goal is to help consumers distinguish between applications that have an endorsement versus applications that have no pedigree (i.e untrusted and could be malicious).

POET uses a <a href="https://jwt.io">JWT</a>, signed with an Endorsing Body's (EB's) private key. The EB's signature can be verified using the EB's public key.


POET payload field definitions are based on <a href="https://tools.ietf.org/html/rfc7519">RFC 7519 - Java Web Token (JWK)</a> and <a href="https://tools.ietf.org/html/rfc7591">OAuth 2.0 Dynamic Client Registration Protocol</a>. Although designed to facilitate trust in OAuth2 clients,  POET can be used for non-OAuth application endorsement. Implementers may add to the payload as they see fit so long as the minimum required fields are kept.

POET's public key format is <a href="https://tools.ietf.org/html/rfc7517">JSON Web Key (JWK)</a>.


The information in the POET endorsement JWT is to be displayed by an OAuth2 Provider in the Authorization flow (when a user approves an application to access his or her own information).  The intended use is for the information to be displayed to end users **prior** to authorizing an application.  OAuth Providers may display a warning message when no endorsement JWTs are present for a given application (e.g. an OAuth2 client). 

POET provides a technical means for another party to _vouch for_ or _endorse_ an OAuth2 application. For example, the organizations, _Transparent Health_ and _UPMC_ could endorse the application _Cardiac Risk App_. In this example, _Transparent Health_ and _UPMC_ are both "Endorsing Bodies (EB)”. An EB digitally signs a special file, called a _JWT_, that contains information about the OAuth2 application.  Information contained within the JWT includes the application's redirect URIs and other basic information.  This JWT payload is further described below.


How Does POET Work for Endorsing Bodies (EBs)?
----------------------------------------------

1. An Endorsing Body is identified as the Issuer `iss` in the JWT's payload. 
2. The Issuer `iss` shall be a fully qulified domain name (FQDN). It's used to locate the EB's public key on the Internet.
1.	A developer provides the Endorsing Body (EB) with information about the application. 
2.	This information includes many of the same elements used in an OAuth client application registration. Most notably the `client_name`, `logo_uri`, are `redirect_uris` are defined.
3.	When approved by the EB, these values become memorialized within the payload of a signed JWT.
4.	The JWT is given to the developer.
5.	The EB may also publish a list of all the applications it endorses.
6.	EBs must sign the JWT with its own private key.
7.	EBs must publish the corresponding public key at `https://[iss]/.well-known/poet.jwk`


How Does POET Work for Developers?
----------------------------------
1. A developer registers his or her application with the Endorsing Body (EB).
2. When approved by the EB, the EB creates a JWT signed by the EB and provides it to you.
3. Share your endorsement: Register the JWT your with your data providers and/or application registries.

How Does POET Work for Data Providers?
--------------------------------------

1. Data Providers may choose to honor only signed JWTs from issuers (`iss`) they trust.
2. A Data Provider is typically both an Auth Server and a Resource Sever. Applications are registered here by developers.
3. An endorsement matching registered applications may be added by supplying the JWT.
4. The JWT may be provided directly by the developer.
5. The JWT may be obtained and associated with registered applications by other means such as a manifest file or API.
6. Data Providers use the presence (and absence) of endorsements to display appropriate information to the end-user. For example is the signature valid, is it un
7. Endorsements should be displayed to the end-user during the authorization/approval process.
8. Data Providers must: a.) verify the JWT signature, b.) verify the endorsement is not expired, c.) if using OAuth2, verify the `software_id` in th JWT matches the uri registered with the OAuth2 provider.


Example POET
============

Example JWT
----------

The  example signed JWT (JWS) contains information about the _Cardiac Risk App_ OAuth2 application and is signed by _transparenthealth.org.org_. The JWS is signed with a private key using the `RS256 Algorithm`.  The corresponding public key shall be <a href="https://tools.ietf.org/html/rfc7517">JWK</a> stored at `https://[iss]/.well-known/poet.jwk`.

    eyJraWQiOiJlbmRvcnNlbWVudHMudHJhbnNwYXJlbnRoZWFsdGgub3JnIiwiYWxnIjoiUlMyNTYiLCJ0eXAiOiJKV1QifQ.eyJsb2dvX3VyaSI6Imh0dHBzOi8vZ2FsbGVyeS5zbWFydGhlYWx0aGl0Lm9yZy9pbWcvYXBwcy82Ni5wbmciLCJpYXQiOjE1MDA0OTIwNjQsInJlZGlyZWN0X3VyaXMiOlsiaHR0cHM6Ly9hcHBzLWRzdHUyLnNtYXJ0aGVhbHRoaXQub3JnL2NhcmRpYWMtcmlzay8iXSwiZXhwIjoxNTYzNTY0MDY0LCJjbGllbnRfdXJpIjoiaHR0cHM6Ly9hcHBzLWRzdHUyLnNtYXJ0aGVhbHRoaXQub3JnL2NhcmRpYWMtcmlzay8iLCJpc3MiOiJlbmRvcnNlbWVudHMudHJhbnNwYXJlbnRoZWFsdGgub3JnIiwic29mdHdhcmVfaWQiOiI0TlJCMS0wWFpBQlpJOUU2LTVTTTNSIiwiZ3JhbnRfdHlwZXMiOlsiYXV0aG9yaXphdGlvbl9jb2RlIl0sImluaXRpYXRlX2xvZ2luX3VyaSI6Imh0dHBzOi8vYXBwcy1kc3R1Mi5zbWFydGhlYWx0aGl0Lm9yZy9jYXJkaWFjLXJpc2svbGF1bmNoLmh0bWwiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIHBhdGllbnQvKi5yZWFkIiwiY2xpZW50X25hbWUiOiJDYXJkaWFjIFJpc2sgQXBwIiwidG9rZW5fZW5kcG9pbnRfYXV0aF9tZXRob2QiOiJjbGllbnRfc2VjcmV0X2Jhc2ljIn0.jcAig3s45Z3W0i6mKXaJCLP1QgVhnDvUTooSXiiIr6tAG7hsGlJo6I3-MD7gH78sCFDuOCHC_HZaLKQL00L5ma4qcA8KwTTboXkorFCLdqp3YIffKOZQZPupBvafkifHoW2vyG7kAVSlzHo-x-rf3N_lCV5gGzXYbGMZ75ss0_F0nfyZTEFUh8GxcAMfJh9Q6ojzaCt9FA3bAvwqJDCuGbSltYawEMTc1gN2OEog213JYZ9A2IIEB3GrSfkEHsJyFdj2nWgOhB2LlnN7N7sbYTaKfMWHQEHUXvm8HK7jc6axUWVkZxFVomnWC2ZGV4H1l68iV4FTYqooZkggrkftgA




Example Header
--------------

    {
    "alg": "RS256",
    "typ": "JWT",
    "kid": "endorsements.transparenthealth.org"
    }

Example Payload
---------------

    {
      "scope": "openid profile patient/*.read",
      "software_id": "4NRB1-0XZABZI9E6-5SM3R",
      "redirect_uris": [
        "https://apps-dstu2.smarthealthit.org/cardiac-risk/"
      ],
      "exp": 1563564064,
      "client_uri": "https://apps-dstu2.smarthealthit.org/cardiac-risk/",
      "initiate_login_uri": "https://apps-dstu2.smarthealthit.org/cardiac-risk/launch.html",
      "iat": 1500492064,
      "iss": "endorsements.transparenthealth.org",
      "client_name": "Cardiac Risk App",
      "grant_types": [
          "authorization_code"
      ],
      "token_endpoint_auth_method": "client_secret_basic",
      "logo_uri": "https://gallery.smarthealthit.org/img/apps/66.png"
    }



Key Responsibilities of an Endorsing Body (EB)
===============================================


* To verify application owners own their domains to which they are binding applications (i.e. `whois`).
* To verify that SSL and valid certificates are in place on the application's server. For example, `https://apps-dstu2.smarthealthit.org` must have a "green light" (e.g. it may not generate common web browser warnings).
* To sign certificates with a private  key with the CN bound to the CB's domain.
* To host the corresponding public key at http(s)://{{iss}}/.well-known/poet.jwks


Payload Fields
==============

 Field names follow RFC  <a href="https://tools.ietf.org/html/rfc7519">7519</a> and RFC <a href="https://tools.ietf.org/html/rfc7591">7591</a>.  Some fields are optional while in other cases, the key is required, but the value can be blank (e.g. `""`, `[]`).

| Field   |     Description   |  Required | Possible Values | Cardinatlity |
|----------|-------------|------|------|------|
| `client_name` |  Name of the client app. See https://tools.ietf.org/html/rfc7591#section-2 | Y | String | 1..1
| `iss` | Issuer: See https://tools.ietf.org/html/rfc7519#section-4.1.1|Y| String of a FQDN | 1..1
| `iat` | Issued At: See https://tools.ietf.org/html/rfc7519#section-4.1.6| Y|Integer|1..1
| `exp` | Expiration Time: https://tools.ietf.org/html/rfc7519#section-4.1.4 |Y|Integer|1..1
| `software_id`| Software ID: A string identifier for the software that comprises a client.|N|String|1..1
|`client_uri`|Client URI: See https://tools.ietf.org/html/rfc7591#section-2|N|String|1..1
|`logo_uri`|Logo URI: See https://tools.ietf.org/html/rfc7591#section-2.2|N|String|1..1
|`redirect_uris`|OAuth2 Redirect URIs: See See https://tools.ietf.org/html/rfc7591|Y|Array of Strings containing URIs. At least 1 value is required for an OAuth2 application.|0..N
|`scope`|OAuth2 Scopes: See See https://tools.ietf.org/html/rfc7591|Y|String with whitespace as seperator. Blank allowed.|1..1
|`token_endpoint_auth_method`|Token Endpoint Auth Method: see https://tools.ietf.org/html/rfc7591#section-2 At least 1 value is required for an OAuth2 application.|Y|String. Possible values are: [`none`, `client_secret_post`, `client_secret_basic`]|1..1
|`grant_types`|Grant Types: See https://tools.ietf.org/html/rfc7591#section-2|Y|Array of Strings. Possible values are:[ `authorization_code`, `implicit`, `password`, `client_credentials`, `refresh_token`].|0..N




Special Instructions for Payload Fields in Non-OAuth2 Applications
------------------------------------------------------------------

When using POET for non-OAuth2 applications, certain keys should still be present, but set to `""` or an empty list `[]`.  The following table outlines the approprite values by field:

| Field   |     Value   |
|---------|-------------|
|`redirect_uris`|`[]`|
|`scopes`|`""`|
|`token_endpoint_auth_method`|`"none"`|
|`grant_types`|`[]`|


Communicating POET JWTs with OAuth 2.0 Dynamic Registration
===========================================================


The POET profile defines one optional, additional field for RFC 7591, OAuth 2.0 Dynamic Registration:  `poet_jwt_endorsement` contains an array of POET JWT endorsements.


                    "client_name": "Cardiac Risk App",
                    "client_uri": "https://apps-dstu2.smarthealthit.org/cardiac-risk/",
                    "logo_uri": "https://gallery.smarthealthit.org/img/apps/66.png",
                    "software_id": "cadiac-risk-app",
                    "redirect_uri": ["https://apps-dstu2.smarthealthit.org/cardiac-risk/redirect"],
                    ...
                    "poet_jwt_endorsement": ["JWT1", "JWT2"]


`JWT1`, `JWT2`, are replaced with actual valid JWT strings. See the Example JWT above.

