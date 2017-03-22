Pre-OAuth Entity Trust (POET) - DRAFT
======================================

The purpose of POET is to assert some level of confidence in 3rd-party applications accessed via OAuth2 using a <a href="https://jwt.io">JWT</a> signed with a private key.

POET was concieved by the Blue Button API Team at the Centers for Medicare and Medicaid Services (CMS) to help Medicare beneficiaries distinguish between applications that have some dsort of endorsement versus applications that have no know pedigree and and could be malicious.

The information in the POET Endorsement JWT can be displayed by an OAuth2 Provider in the Authorization flow (when a user approves an applicaition to access his or her own information).  The intended use is for the information to be displayed to end users **prior** to authorizing an application.  OAuth Providers may display a warning message when no endorsements JWTs are present for a given application (i.e. an OAuth2 client).

POET provides a technical means for another party to _vouch for_ or _endorse_ an OAuth2 application. For example, the organizations, _NATE Trust_ and _UPMC_ could endorse the application _Cardiac Risk App_. In this example, _NATE_ and _UPMC_ are both "Endorsers". An Endorser digitally signs a special file, called a _JWT_, that contains information about the OAuth2 application.  Information contained within the JWT includes the application's redirect URIs and other basic information.  This JWT payload is further described below.


How Does it Work?
-----------------


1.	A developer registers his or her application with the Endorsing Body (EB). Information collected includes many of the same elements used in an oAuth client application registration.  Items include the name, host name, and redirect URLs of the application.
2.	When approved by the EB, these values become memorialized and are embedded into a signed JWT, containing a software statement, that is given to the developer.  The EB's application registry contains one JSON document per certified application.
3.	An OAuth2 Server (OAuth2 Provider) may obtain a list of JWTs (i.e. a manifest) from a central source such as URL. Optionally, when an application developer is registering an application in the OAuth2 server, he or she may optionally include one or more JWT to the application registration as a software statement (?).  The endorsement badge information will be displayed to the developer upon registration.
4.	The badge and related information will be displayed to the end-user at the point of the oAuth2 client authorization.
5.	While we anticipate all 3rd party applications will contain warnings to the end-user, when one or more valid badges are present, the warning language will be lessened. In the green, yellow, red, analogy the warning would become yellow.


Example  JWT
------------

The  example signed JWT (JWS) contains infromation about the _Cardiac Risk App_ OAuth2 application and is signed by _nate-trust.org_.
The JWS is signed with a private key using the `RS256 Algorithm`.  The corresponding public key, whether an X509 certificate or a JWKS, shall be stored at the stored at the URI found in the `poet_public_key_uri` in the payload.  The 
`poet_public_key_uri` must be the same domain or a subdomain as the domain found in `iss`.  For example, if the `iss` is `https://nate-trust.org`, then acceptable value for the `poet_public_key_uri` include `https://nate-trust.org/.well-known/poet.pem`.  `https://subdomain.nate-trust.org/.well-known/poet.pem`, `https://nate-trust.org/.well-known/poet.jwks` and `https://another-subdomain.nate-trust.org/.well-known/poet.jwks`. If the `poet_public_key_uri` is omitted from the payload, clients can check the default locaction of the private key: `[iss]/.well-known/poet.pem` or  `[iss]/.well-known/poet.jwks`.


Example Header
--------------

    {
    "alg": "RS256",
    "typ": "JWT"
    }

Example Payload
---------------

    {
    "software_id": "4NRB1-0XZABZI9E6-5SM3R",
    "iss": "https://nate-trust.org",
    "iat": 1455031265,
    "exp": 1549639265,
    "client_name" : "Cardiac Risk App",
    "client_uri": "https://apps-dstu2.smarthealthit.org/cardiac-risk/",
    "logo_uri" : "https://gallery.smarthealthit.org/img/apps/66.png",
    "initiate_login_uri" : "https://apps-dstu2.smarthealthit.org/cardiac-risk/launch.html",
    "redirect_uris" : [
          "https://apps-dstu2.smarthealthit.org/cardiac-risk/"
       ],
    "scope" : "openid profile patient/*.read",
    "token_endpoint_auth_method" : "none",
    "grant_types" : [ "authorization_code" ]
    "poet_public_key_uri": "https://nate-trust.org/.well-known/poet.pem"
    }


Example Signature
-----------------

    HMACSHA256(
      base64UrlEncode(header) + "." +
      base64UrlEncode(payload),
    ) secret base64 encoded


Example JWT
-----------

    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJuYXRlLXRydXN0Lm9yZyIsImlhdCI6MTQ1NTAzMTI2NSwiZXhwIjoxNTQ5NjM5MjY1LCJhdWQiOiJhcHBzLWRzdHUyLnNtYXJ0aGVhbHRoaXQub3JnIiwic3ViIjoianJvY2tldEBhcHBzLWRzdHUyLnNtYXJ0aGVhbHRoaXQub3JnIiwiY2VydGlmaWNhdGlvbl91aWQiOiI5MjkyMDEwMTMxIiwiY29udGFjdHMiOlsiaW5mb0BzbWFydHBsYXRmb3Jtcy5vcmciLCJodHRwczovL2dhbGxlcnkuc21hcnRoZWFsdGhpdC5vcmciXSwiY2xpZW50X25hbWUiOiJDYXJkaWFjIFJpc2sgQXBwIiwiY2xpZW50X3VyaSI6Imh0dHBzOi8vYXBwcy1kc3R1Mi5zbWFydGhlYWx0aGl0Lm9yZy9jYXJkaWFjLXJpc2svIiwibG9nb191cmkiOiJodHRwczovL2dhbGxlcnkuc21hcnRoZWFsdGhpdC5vcmcvaW1nL2FwcHMvNjYucG5nIiwiaW5pdGlhdGVfbG9naW5fdXJpIjoiaHR0cHM6Ly9hcHBzLWRzdHUyLnNtYXJ0aGVhbHRoaXQub3JnL2NhcmRpYWMtcmlzay9sYXVuY2guaHRtbCIsInJlZGlyZWN0X3VyaXMiOlsiaHR0cHM6Ly9hcHBzLWRzdHUyLnNtYXJ0aGVhbHRoaXQub3JnL2NhcmRpYWMtcmlzay8iXSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBwYXRpZW50LyoucmVhZCIsInRva2VuX2VuZHBvaW50X2F1dGhfbWV0aG9kIjoibm9uZSIsImdyYW50X3R5cGVzIjpbImF1dGhvcml6YXRpb25fY29kZSJdfQ.0E4c0g4JTz2Fbr9oxp7RdMtJ5LqrVHuYOmvh7D6MHCE



Key Responsibilities of an Endorsing Body (EB)
===============================================


* To verify application owners own their domains to which they are binding applications (i.e. `whois`).
* To verify that SSL and valid certificates are in place on the application's server. For example, `https://apps-dstu2.smarthealthit.org` must have a "green light" (e.g. it may not generate common web browser warnings).
* To sign certificates with a private  key with the CN bound to the CB's domain.
* To host the corresponding public key at http(s)://{{iss}}/wellknown/poet.pem or http(s)://{{iss}}/wellknown/poet.jwks


List of All Fields in the Payload
=================================

 Field names follow RFC 7591, OAuth 2.0 Dynamic Registration. See https://tools.ietf.org/html/rfc7591 for details.


    * software_id: A string identifier for the software that comprises a client.
    * iss: A string containing a FQDN. See https://tools.ietf.org/html/rfc7591
    * iat: An integer representing the epoch of the time the JWT was signed.
    * exp: An integer representing the epoch of the time the JWT will expire.
    * client_name: See https://tools.ietf.org/html/rfc7591#section-2.2 
    * client_uri: See https://tools.ietf.org/html/rfc7591#section-2.2
    * logo_uri :  See https://tools.ietf.org/html/rfc7591#section-2.2
    * initiate_login_uri: A string containing a URI pointing to the client's login.
    * redirect_uris: See https://tools.ietf.org/html/rfc7591
    * scope : See https://tools.ietf.org/html/rfc7591
    * token_endpoint_auth_method: A string  enumeration. ["none", "client_secret_post", "client_secret_basic"]
    * grant_types : A string  enumeration.[ "authorization_code", "implicit", "password", "client_credentials", "refresh_token" ]


Communicating POET JWTs in an OAuth 2.0 Dynamic Registration Scenerio
=====================================================================

POET endorsement JWTs are meant to be public information that can be given
to application developers and discovered by OAuth2 providers. To promote 
dynamic registration of applications and to avoid the situation where each developer must carry the JWT and register it with each and every OAuth2 Provider, a URL pointing to a JSON document containing a manifest of
one or more  an OAuth2 client application.  OAuth2 Providers may obtain 
URLs from trusted parties or from developers.  The format of the JSON document 
is based on, RFC 7591, OAuth 2.0 Dynamic Registration. This profile defines 
one optional, additional field  `poet_jwt_endorsements` that contains an array of POET JWT endorsements.

The format of the JSON document will be a JSON object with one key, `manifests`,
with an array `[]` key value. Each value in the `manifests` array shall contain additional JSON objects. These additional
objects shall contain one key that is either the value of `sub` or 
`software_id`, or `client_uri` for the application.  The value of the key will conform to RFC 7591, OAuth 2.0 Dynamic Registration, with the additional key `poet_jwt_endorsements`.  Below is an example of an application manifest file containing informationn about 3 applications. The first two contain endorsements while the third has none.


    {
        "manifests": [{
                "https://apps-dstu2.smarthealthit.org/cardiac-risk": {
                    "client_name": "Cardiac Risk App",
                    "client_uri": "https://apps-dstu2.smarthealthit.org/cardiac-risk/",
                    "logo_uri": "https://gallery.smarthealthit.org/img/apps/66.png",
                    "software_id": "cadiac-risk-app",
                    "redirect_uri": ["https://apps-dstu2.smarthealthit.org/cardiac-risk/redirect"],
                    ...
                    "poet_endorsements": ["JWT1", "JWT2"]
                }
            }, {
                "https://apps-dstu2.smarthealthit.org/bp-centiles": {
                    "client_name": "Blood Pressure App",
                    "client_uri": "https://apps-dstu2.smarthealthit.org/bp-centiles",
                    "logo_uri": "https://gallery.smarthealthit.org/img/apps/20.png",
                    "software_id": "blood-pressure-app",
                    "redirect_uri": ["https://apps-dstu2.smarthealthit.org/bp-centiles/redirect"],
                    ...
                    "poet_endorsements": ["JWT3", "JWT4"]
                }
            }, {
                "https://example.com": {
                    "client_name": "App with no endorsements",
                    "client_uri": "https://example.com/",
                    "logo_uri": "https://example.com/img.png",
                    "software_id": "123456789",
                    "redirect_uri": ["https://example.com/redirect"]
                    ...
                }
            }

        ]
    }


`JWT1`, `JWT2`, `JWT3`, `JWT4` would be replaced with actual valid JWT strings. See the Example JWT above. `...` indicates any field allowed by RFC 7591.