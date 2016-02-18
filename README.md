Pre oAuth Entity Trust (POET) (DRAFT - For Discussion Purposes Only)
====================================================================

In an attempt to assert some level of confidence in 3rd party
applications, CMS will use a system, known as Pre oAuth Entity Trust , or POET for short, to allow select certifying bodies to identify applications that are deemed to meet some specific criteria established by the certifying body and/or CMS.

How Does it Work?
-----------------

1. CMS first registers select certifying bodies (CBs). CMS can de-register a CB at any time.
2. A developer will register his or her application with the CB. Information collected includes many of the same elements used in an oAuth client application registration.  Items include the name, host name, and redirect URLs of the application.  When approved by the CB, these values become memorialized and are embedded into a signed JWT, containing a software statement, that is given to the developer. and re the re  The CB's application registry contains one JSON document per certified application.  
3. When an application developer is registering an application in CMS's oAuth server, he or she may optionally include the JWT upon application registration.  The certificate badge information will be displayed to the developer upon regitration.
5. The certification information will be displayed to the end-user at the point of the oAuth client authorization.
7. While we anticipate all 3rd party applications will contain warnings to the end-user, when one or more valid certifications are present, but the warning language will be lessened. In the green, yellow, red, analogy the warning would become yellow.


Example  JWT
------------

An example JWS (a signed JWT) for using NATE as the CB and Smart Cardiac Risk App as the client 
application. The JWS is signed with a private certificate bound to the domain `nate-trust.org` 
using the `RS256 Algorithm`.  The corresponding public certificate shall be hosted at 
`https://nate-trust.org/.welknown/??`.  Justin can you speak to what should go here?   


Header
------

    {
    "alg": "HS256",
    "typ": "JWT"
    }

Payload
-------

    {
    "iss": "nate-trust.org",
    "iat": 1455031265,
    "exp": 1549639265,
    "aud": "apps-dstu2.smarthealthit.org",
    "sub": "jrocket@apps-dstu2.smarthealthit.org",
    "certification_uid": "9292010131",
       "contacts" : [
          "info@smartplatforms.org",
          "https://gallery.smarthealthit.org"
       ],
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


Signature
---------

    HMACSHA256(
      base64UrlEncode(header) + "." +
      base64UrlEncode(payload),
      
    ) secret base64 encoded


JWT
---

    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJuYXRlLXRydXN0Lm9yZyIsImlhdCI6MTQ1NTAzMTI2NSwiZXhwIjoxNTQ5NjM5MjY1LCJhdWQiOiJhcHBzLWRzdHUyLnNtYXJ0aGVhbHRoaXQub3JnIiwic3ViIjoianJvY2tldEBhcHBzLWRzdHUyLnNtYXJ0aGVhbHRoaXQub3JnIiwiY2VydGlmaWNhdGlvbl91aWQiOiI5MjkyMDEwMTMxIiwiY29udGFjdHMiOlsiaW5mb0BzbWFydHBsYXRmb3Jtcy5vcmciLCJodHRwczovL2dhbGxlcnkuc21hcnRoZWFsdGhpdC5vcmciXSwiY2xpZW50X25hbWUiOiJDYXJkaWFjIFJpc2sgQXBwIiwiY2xpZW50X3VyaSI6Imh0dHBzOi8vYXBwcy1kc3R1Mi5zbWFydGhlYWx0aGl0Lm9yZy9jYXJkaWFjLXJpc2svIiwibG9nb191cmkiOiJodHRwczovL2dhbGxlcnkuc21hcnRoZWFsdGhpdC5vcmcvaW1nL2FwcHMvNjYucG5nIiwiaW5pdGlhdGVfbG9naW5fdXJpIjoiaHR0cHM6Ly9hcHBzLWRzdHUyLnNtYXJ0aGVhbHRoaXQub3JnL2NhcmRpYWMtcmlzay9sYXVuY2guaHRtbCIsInJlZGlyZWN0X3VyaXMiOlsiaHR0cHM6Ly9hcHBzLWRzdHUyLnNtYXJ0aGVhbHRoaXQub3JnL2NhcmRpYWMtcmlzay8iXSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBwYXRpZW50LyoucmVhZCIsInRva2VuX2VuZHBvaW50X2F1dGhfbWV0aG9kIjoibm9uZSIsImdyYW50X3R5cGVzIjpbImF1dGhvcml6YXRpb25fY29kZSJdfQ.0E4c0g4JTz2Fbr9oxp7RdMtJ5LqrVHuYOmvh7D6MHCE


  1. The CMS oAuth server checks the JWT to determine if the  `certifiying_body_uid` value of `NATE-039848502-02-5854`, and other contents of the JWT.
  

Key Responsibilities of a Certifying Body (CB)
==============================================


* To verify application owners own their domains to which they are binding applications (i.e. `whois`).
* To verify that SSL and valid certificates are in place on the application's server. For example, `https://apps-dstu2.smarthealthit.org` must have a "green light" (e.g. it may not generate common web browser warnings).
  

