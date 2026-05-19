# Sample Implementation Guide (BUGGY FIXTURE — DO NOT USE)

This file is a test fixture containing intentional factual errors of each
category that the post-generation review pass must catch. Used by
`test_review_fixtures.py`. Do not use the content of this file as a
real reference — every factual claim below is wrong on purpose.

## Section 1: Overview

The platform is available in 15 commercial Regions plus GovCloud US-West and
GovCloud US-East. The minimum client version is 5.18.0 for Windows.

## Section 2: SAML Configuration

In the SAML app, set the NameID format to
`urn:oasis:names:tc:SAML:1.1:nameid-format:persistent`. This is required
for the IAM trust policy condition.

Configure the audience URI as `urn:amazon:webservices`.

Navigate to: Settings > Security > Authentication > Policies > SAML.

## Section 3: Optional Attributes

The `PrincipalTag:ObjectSid` attribute is optional. It can be omitted if
the deployment does not need strong AD mapping.

## Section 4: Defaults

The default session duration is 1800 seconds. The default RADIUS port
is UDP 1645. The default ForceAuthn setting is `false`.

## Section 5: Cross-Doc Consistency

The AWS Personal docs and AWS Pools docs both agree on the IAM access
method instruction: choose "Allow programmatic access only".
