# Product Portfolio Map (Solution Mapping)

Use this file to map a customer's stated needs to the right Okta / Auth0 product(s) **before** loading a product-specific reference file — especially when the SE has not named a product, or when the requirements span more than one product domain.

This is the "which product(s) fit this opportunity?" step. It exists so the skill is useful across *any* Okta presales opportunity, not just the one product an SE happened to name. It does **not** change the skill's philosophy: recommend the honest best-fit product(s), name the gaps, and flag where an adjacent product or augmentation is the real answer — never force-fit the portfolio to a need it does not serve.

## The Okta / Auth0 portfolio at a glance

Okta sells two clouds plus a governance layer and several specialized add-ons. The word "Okta" alone is ambiguous — always resolve it to a specific product.

| Product family | What it's for | Reference file |
|----------------|--------------|----------------|
| **Workforce Identity Cloud (WIC)** | Employee/contractor access: SSO, MFA, passwordless, directory, lifecycle, adaptive access | `okta-wic-reference.md` |
| **Okta Identity Governance (OIG)** | Governance on top of WIC: access requests, certifications, entitlements, SoD, JML | `okta-oig-reference.md` |
| **Okta Privileged Access (OPA)** | Privileged/server access: SSH/RDP, ephemeral creds, password & secret checkout, sudo control | `okta-opa-reference.md` |
| **Identity Threat Protection (ITP)** | Continuous, post-auth threat detection & response; Shared Signals Framework | `okta-itp-reference.md` |
| **Okta Device Access** | Okta auth at the OS login of Windows/macOS endpoints (Desktop MFA) | `okta-device-access-reference.md` |
| **Okta Access Gateway (OAG)** | Extend SSO/MFA to on-prem legacy web apps (header/Kerberos/SAML) | `okta-access-gateway-reference.md` |
| **Customer Identity Cloud (CIC), powered by Auth0** | CIAM: consumer/B2B login, Universal Login, connections, Actions, Organizations, M2M | `auth0-cic-reference.md` |
| **Auth0 Fine-Grained Authorization (FGA)** | App-level relationship-based authorization (ReBAC / OpenFGA) | `auth0-fga-reference.md` |

Platforms outside this list (SailPoint, Microsoft Entra, Ping, Saviynt, CyberArk, etc.) route to `research-protocol.md`.

## Needs → Product matrix

Match the customer's language on the left to the product on the right, then load that product's reference file. Customers rarely use product names — listen for the *need*.

| If the customer needs… (signals) | Primary product | Also consider |
|----------------------------------|-----------------|---------------|
| Single sign-on to SaaS apps; one login for employees | **WIC** | OIG (if they also say "reviews/audit") |
| MFA, passwordless, phishing-resistant login for staff | **WIC** (FastPass, Adaptive MFA) | Device Access (if "laptop/OS login") |
| Automated onboarding/offboarding, HR-driven provisioning (JML) | **WIC** (LCM) + **OIG** | — |
| Access requests, approvals, access reviews, certifications, SoD, "audit / compliance / SOX" | **OIG** | WIC (foundation) |
| Secure admin access to servers, SSH/RDP, "vault," password/secret checkout, sudo control | **OPA** | OIG (governing who can request) |
| Detect compromised sessions, respond to risk after login, EDR/security-signal sharing | **ITP** | WIC (base policies) |
| MFA at Windows/macOS login, secure the endpoint sign-in | **Device Access** | WIC |
| SSO/MFA for old on-prem web apps that can't do SAML/OIDC | **OAG** | WIC |
| Login for *customers/consumers*, sign-up, social login, B2B tenants, developer-embedded auth | **CIC (Auth0)** | Auth0 FGA (if "who-can-access-what in-app") |
| Fine-grained "who can view/edit this document/resource" inside an app; sharing permissions at scale | **Auth0 FGA** | CIC (Auth0) for authN |

**The single most important split:** *workforce* (employees/contractors accessing company apps → WIC family) vs *customer/consumer* (end users of the customer's own product → CIC/Auth0). Get this right first; everything else follows.

## How to use this in the skill (Phase 3)

1. If the SE named a specific product, skip straight to that product's reference file — no need to map.
2. If the product is unspecified or the word "Okta" is ambiguous, or the requirements clearly span multiple domains: use the matrix above to **recommend** the product(s), then **confirm with the SE** before generating. Example:
   > Based on these requirements, this looks like **Okta WIC** (for SSO + MFA) plus **OIG** (for the quarterly access reviews you mentioned). Does that match how you're positioning it, or is a different product in scope?
3. Load the reference file(s) for the confirmed product(s). For a multi-product guide, load **each** relevant file and organize sections by product/domain.
4. Then run the standard Phase 3 current-state validation (`web_search` + `web_fetch` the live vendor docs) before generating — the reference files are priors, not the source of truth.

## Multi-product opportunities

Real deals often span products. When they do, build one guide with sections mapped to each product, and make the boundaries explicit so the customer understands what each product does:

- **Workforce SSO + Governance:** WIC (access) + OIG (requests/certifications) — the most common pairing.
- **Governance + Privileged Access:** OIG (who should have access) + OPA (how privileged sessions are brokered).
- **Access + Threat Response:** WIC + ITP (continuous evaluation after login).
- **CIAM + In-app Authorization:** CIC/Auth0 (authentication) + Auth0 FGA (fine-grained authorization).
- **Endpoint-to-cloud:** Device Access (OS login) + WIC (app SSO).

For each product in a multi-product guide, load its reference file and follow that file's use-case patterns and honest capability assessment. Do not blur two products into one set of components.

## Keep it honest

Solution mapping is a recommendation aid, not a sales script. If a need is a poor fit for the portfolio (or better served by a partner/adjacent product, or requires meaningful augmentation via Okta Workflows or custom integration), say so as a discovery item. An SE who hears "this part isn't a native fit — here's what it would take" trusts every other recommendation more. That trust is the actual presales asset.
