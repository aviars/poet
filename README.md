# poet
Pre-OAuth Entity Trust API

# Specification

The POET Specification is posted here: https://github.com/ekivemark/poet/POET_specification.md

The PDF of a presentation given to the DirectTrust Security and Trust Work Group on December 10th, 2015 
can be found here: https://github.com/ekivemark/poet/POET_Intro.pdf

A blog post introducing POET (then called a Whitelist Trust API can be found here:
- "Trusting Health APIs" http://www.hhs.gov/idealab/2015/11/19/trusting-health-apis/
with a copy on my personal blog here: 
- http://blog.ekivemark.com/developing-trust-for-health-apis-inc-bluebutton-and-bbonfhir/

# What is POET

Modern APIs use OAuth 2.0 to securely authorize third party applications to consumer or publish data via APIs. 
This practice is finally spreading to Federal Healthcare. However, Federal Agencies are charged with protecting
Beneficiary health information and they take this responsibility extremely seriously. In this situation an important
issue emerges with OAuth: Who do you trust with the keys to the data. 

While OAuth requires an AUTHENTICATED user to give specific AUTHORIZATION to a third party application there is still
the question of "Can we trust the third party application as a "Good Actor." This is the issue that POET sets out to
address. In Healthcare the adoption of secure Messaging using the Direct Protocol has resulted in "Communities of Trust"
emerging. Within these communities entities have been validated and can securely exchange information as necessary. 
POET seeks to leverage these Communities of Trust by using a simple API to check with the administrators of these
communities to determine if a developer organization is known to the community. If the developer organization is known
then they can be trusted with the ability to create OAuth keys and secrets. 

To be clear, even after passing the POET Validation the developer has no access to data. POET validation is a gate that
they pass which lets them create OAuth credentials. They then embed those credentials in their application. A beneficiary,
or data subject, can then choose to connect to the Data Publisher that required the POET Validation. The data subject
must then explicitly authenticate and authorize the third party application's access to their data. This is the standard
OAuth process flow. It is only at this point that a third party application has access to that specific individual's 
information and only to the segments of their data that the data subject explicitly allowed.

# The bottom line

The POET (Pre-Oauth Entity Trust) API provides a mechanism for an organization who publishes a health API to use 
established Health Communities of Trust to confirm that a third party application development organization is known 
to the community.


 
 


