Pre-OAuth Entity Trust (POET) - DRAFT
======================================

POET was conceived by the Blue Button API Team at the Centers for Medicare and Medicaid Services (CMS) to help Medicare beneficiaries distinguish between applications that have some sort of endorsement versus applications that have no pedigree (i.e untrusted and could be malicious).

POET uses a <a href="https://jwt.io">JWT</a> ,signed with an Endorsing Body's private key. POET field definitions for its payload are use  <a href="https://tools.ietf.org/html/rfc7519">RFC 7519</a> and 
<a href="https://tools.ietf.org/html/rfc7591">RFC 7591</a>. Other field definitions are defined in this document. POET can be used for non-OAuth application endorsement. Implementers may add to the payload as they see fit.

The information in the POET endorsement JWT is to be displayed by an OAuth2 Provider in the Authorization flow (when a user approves an application to access his or her own information).  The intended use is for the information to be displayed to end users **prior** to authorizing an application.  OAuth Providers may display a warning message when no endorsement JWTs are present for a given application (e.g. an OAuth2 client). 

POET provides a technical means for another party to _vouch for_ or _endorse_ an OAuth2 application. For example, the organizations, _NATE Trust_ and _UPMC_ could endorse the application _Cardiac Risk App_. In this example, _NATE_ and _UPMC_ are both "Endorsing Bodies (EB)”. An EB digitally signs a special file, called a _JWT_, that contains information about the OAuth2 application.  Information contained within the JWT includes the application's redirect URIs and other basic information.  This JWT payload is further described below.


How Does POET Work for Endorsing Bodies (EBs)?
----------------------------------------------

1.	A developer provides the Endorsing Body (EB) with information about the application. 
2.	This information includes many of the same elements used in an OAuth client application registration. Most notably the `client_name`, `logo_uri`, are `redirect_uris` are defined.
3.	When approved by the EB, these values become memorialized within the payload of a signed JWT,
4.	The JWT is given to the developer.
5.	The EB may also publish a list of all the applications it endorses.
6.	EBs must sign the JWT with a private key.
7.	EBs must publish the corresponding public key at `example.com/.well-known/poet.jwks` or `/.well-known/poet.pem`.


How Does POET Work for Developers?
----------------------------------
1. A developer registers his or her application with the Endorsing Body (EB).
2. When approved by the EB, the EB creates a JWT signed by the EB and provides it to you.
3. Share your endorsement: Register the JWT your with your data providers and/or application registries.

How Does POET Work for Data Providers?
--------------------------------------

2.	1.	A Data Provider is typically both an Auth Server and a Resource Sever. Applications are registered here by developers.
2. An endorsement matching registered applications may be added by supplying the JWT.
3. The JWT may be provided directly by the developer.
4. The JWT may be obtained and associated with registered applications by other means such as a manifest file or API.
5. Data Providers use the presence (and absence) of endorsements to display appropriate information to the end-user. For example is the signature valid, is it un
6. Endorsements should be displayed to the end-user during the authorization/approval process.
7. Data Providers must: a.) verify the JWT signature, b.) verify the endorsement is not expired, c.) if using OAuth2, verify the `redirect_uri` in th JWT matches the uri registered with the OAuth2 provider.
8. JWT verification in JavaScript browser-based applications is discouraged as it could pose a security risk.


Example POET JWT
----------------

The  example signed JWT (JWS) contains information about the _Cardiac Risk App_ OAuth2 application and is signed by _nate-trust.org_.
The JWS is signed with a private key using the `RS256 Algorithm`.  The corresponding public key, whether an X509 certificate or a JWKS, shall be stored at the stored at the URI found in the `poet_public_key_uri` in the payload. Clients can discover the POET public key URI from the `iss` field.  Check  `[iss]/.well-known/poet.jwks` and if that is not found, check the `[iss]/.well-known/poet.pem`.


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
* To host the corresponding public key at http(s)://{{iss}}/.well-known/poet.pem or http(s)://{{iss}}/.well-known/poet.jwks


List of All Fields in the Payload
=================================

 Field names follow RFC  <a href="https://tools.ietf.org/html/rfc7519">7519</a> and RFC <a href="https://tools.ietf.org/html/rfc7591">7591</a>.

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

