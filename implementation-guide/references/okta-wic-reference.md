# Okta Workforce Identity Cloud (WIC) Reference

## Platform Components

Use these component names consistently across all documents. Map use cases to the appropriate components.

### Core Components

| Component | What It Does | Common Use Cases |
|-----------|-------------|------------------|
| **Single Sign-On (SSO)** | Authenticates users once and grants access to multiple apps via SAML, OIDC, WS-Federation, or SWA | Reducing password fatigue, centralizing app access, securing SaaS sprawl |
| **Universal Directory (UD)** | Centralized, extensible user/group store with custom attributes and profile mappings across sources | Single source of identity truth, attribute-based access, org restructuring |
| **Adaptive Multi-Factor Authentication (Adaptive MFA)** | Risk-based MFA that evaluates device, location, network, and behavior signals to decide when to challenge | Step-up authentication, reducing MFA fatigue, impossible-travel detection |
| **Okta Verify** | Okta's native authenticator app — supports push notifications, TOTP, and biometric/PIN unlock | General-purpose MFA factor across desktop and mobile |
| **Okta FastPass** | Phishing-resistant, passwordless authentication delivered through Okta Verify, using public key cryptography and device biometrics (Windows Hello, Touch ID, Face ID) | Passwordless workforce sign-in, phishing resistance, Zero Trust initiatives |
| **Authentication Policies (App Sign-In Policies)** | Per-application rules defining which factors/conditions are required to access a specific app or group of apps | App-specific MFA requirements, contextual access rules, exempting trusted networks |
| **Global Session Policy** | Tenant-wide policy governing the primary authentication step and session lifetime before app-level policies apply | Baseline session timeout, primary factor requirements, org-wide network/device gating |
| **Okta ThreatInsight** | Aggregates cross-tenant sign-in telemetry to detect and optionally block credential-stuffing/password-spray IPs | Brute-force mitigation, blocking known-malicious IPs at the door |
| **Lifecycle Management (LCM)** | Automated joiner/mover/leaver provisioning and deprovisioning driven by HR or directory events | Onboarding, role changes, offboarding (see OIG reference for deep JML detail) |
| **SCIM Provisioning** | Standards-based protocol for automated create/update/deactivate of user accounts in downstream apps | Automated app account lifecycle, entitlement sync |
| **Okta Workflows** | No-code/low-code automation and orchestration engine with 100+ connectors and a visual flow builder | Custom onboarding logic, notifications, cross-system data sync |
| **Okta Integration Network (OIN)** | Catalog of thousands of pre-built app integrations for SSO, provisioning, and lifecycle management | Rapid app onboarding without custom integration work |
| **API Access Management** | Add-on that lets customers create custom OAuth 2.0 authorization servers to secure their own APIs | Securing first-party APIs, issuing scoped access tokens to client apps |
| **Device Trust / Device Assurance Policies** | Checks device security posture (OS version, patch level, disk encryption, screen lock, jailbreak/root status) as a sign-in condition | Managed-device requirements, BYOD risk gating, compliance-driven access rules |

### Supporting Components

| Component | What It Does | Common Use Cases |
|-----------|-------------|------------------|
| **Network Zones** | Named IP ranges/geolocations referenced by policies | Geo-fencing, trusted-office-network exemptions |
| **Behavior Detection Rules** | Flags anomalies like new device, new location, or new IP compared to user history | Step-up triggers, risk scoring inputs |
| **Inline Hooks** | Real-time callouts during authentication/registration for custom logic | Custom password validation, token enrichment, registration checks |
| **Event Hooks** | Async notifications to external systems when Okta events occur | SIEM integration, custom notification systems |
| **Okta Expression Language (OEL)** | Attribute transformation language for profile mappings and policy conditions | Username generation, conditional profile logic |
| **Directory Integrations (AD/LDAP via Okta AD/LDAP Agent)** | On-premises directory sync into Universal Directory | Hybrid environments with on-prem AD as a source of truth |
| **Okta Access Gateway (OAG)** | Extends SSO/MFA to legacy on-prem and header-based apps that predate modern SSO protocols | Legacy app modernization without app code changes |

### Important Distinctions

**Okta Verify push ≠ Okta FastPass**
- **Okta Verify push**: A traditional MFA factor — the user approves a push notification as a second factor, typically after a password prompt.
- **Okta FastPass**: A phishing-resistant, passwordless primary authenticator built into Okta Verify, using public/private key pairs bound to the device. It can replace password + MFA entirely, not just serve as a second factor.
- They share an app (Okta Verify) but are functionally distinct authentication methods. Don't market push notifications as "phishing-resistant" — only FastPass (and other WebAuthn/FIDO2 factors) carry that designation.

**Global Session Policy ≠ Authentication Policy (App Sign-In Policy)**
- **Global Session Policy**: Tenant-wide. Governs the user's primary Okta session — how they first authenticate and how long that session lasts before re-prompting. Every user is subject to exactly one evaluated global session policy.
- **Authentication Policy**: App-specific (or app-group-specific). Layered on top of the global session policy to add per-application requirements (e.g., "Finance apps require FastPass and a managed device").
- A user must pass the global session policy before app sign-in policies are even evaluated. Confusing the two leads to conflicting or redundant rule design.

**WIC vs OIG**
- **Workforce Identity Cloud (WIC)**: The access-management platform — authentication, SSO, MFA, lifecycle provisioning, and the automation/integration fabric around them. This file.
- **Okta Identity Governance (OIG)**: Governance capabilities layered on WIC — access certifications, access requests (RCAR), entitlement management, and SoD. See `okta-oig-reference.md`.
- LCM/SCIM provisioning lives conceptually in both: WIC executes the provisioning, OIG governs and certifies what was provisioned. Don't duplicate governance detail here — cross-reference the OIG file.

**Adaptive MFA ≠ a single factor**
- Adaptive MFA is a policy capability (risk-based enforcement), not a factor itself. It decides *when* and *which* factors to require — the factors themselves are Okta Verify, FastPass, WebAuthn security keys, SMS/voice, etc.

---

## Common WIC Use Case Patterns

### Workforce SSO to SaaS Apps

**Typical flow:**
User navigates to app or Okta End-User Dashboard → Global Session Policy evaluated → Authentication Policy evaluated for the app → SSO assertion (SAML/OIDC) issued → User lands in app authenticated

**Key Okta components:** Single Sign-On, Universal Directory, Authentication Policies, Global Session Policy, Okta Integration Network

**Discovery questions:**
- Which apps are in scope, and are they in the OIN catalog or will they need custom SAML/OIDC/SWA configuration?
- Do any apps require SP-initiated vs IdP-initiated flows?
- Are there apps still using legacy protocols (header-based auth, Kerberos) that may need Okta Access Gateway?
- What is the desired end-user landing experience (dashboard, deep link, chained redirect)?
- Are there app-specific session timeout or re-authentication requirements?

### Adaptive & Step-Up MFA

**Typical flow:**
Sign-in attempt → Risk signals evaluated (device, location, network, behavior) → Policy determines required factor(s) → User challenged if risk/context requires → Access granted or denied

**Key Okta components:** Adaptive MFA, Authentication Policies, Okta ThreatInsight, Behavior Detection Rules, Network Zones

**Discovery questions:**
- What factors are currently in use, and which are acceptable for which risk tiers?
- Which apps or actions require step-up (e.g., payroll changes, admin console access)?
- Are there user populations exempt from MFA today, and is that intentional or a gap?
- What is the tolerance for user friction vs. security posture (executive pushback is common here)?
- Should trusted networks (corporate offices) reduce MFA frequency, and how is "trusted" defined?

### Phishing-Resistant Passwordless (FastPass)

**Typical flow:**
User enrolls Okta Verify on a managed/registered device → FastPass key pair generated and bound to device → Sign-in attempt triggers FastPass challenge → Biometric/PIN unlock on device → Phishing-resistant assertion returned to Okta

**Key Okta components:** Okta FastPass, Okta Verify, Device Assurance Policies, Authentication Policies

**Discovery questions:**
- What device platforms are in scope (Windows, macOS, iOS, Android), and are they MDM-managed or BYOD?
- Is there an existing device management platform (Intune, Jamf, Workspace ONE) FastPass needs to align with?
- What is the fallback factor for unsupported devices or during enrollment gaps?
- Is there a phishing-resistance compliance mandate (e.g., cyber insurance, federal/EO requirements) driving urgency?
- What is the rollout strategy — pilot group first, or org-wide cutover with a grace period?

### Automated App Provisioning

**Typical flow:**
User assigned to app (directly or via group rule) → SCIM/API provisioning connector triggered → Account created/updated in target app → Entitlements pushed if supported → Deprovisioning on unassignment

**Key Okta components:** SCIM Provisioning, Okta Integration Network, Lifecycle Management, Okta Workflows (for apps without native provisioning support)

**Discovery questions:**
- Does the target app have a SCIM/API-based OIN integration, or will this require a custom Workflows connector or on-prem agent (Generic DB/LDAP)?
- What attributes need to flow to the app, and where do they originate (HRIS, AD, manual entry)?
- Is entitlement-level provisioning needed (roles, permission sets) or account-creation only?
- What is the deprovisioning behavior expected — immediate deactivation, delayed deletion, or data retention hold?
- Who owns break/fix when provisioning fails (connector errors, attribute mapping mismatches)?

### Self-Service Password Reset

**Typical flow:**
User initiates forgot-password → Identity verified via recovery factor(s) → Password reset per policy complexity rules → Session re-established

**Key Okta components:** Authentication Policies (recovery settings), Okta Verify/factors, Universal Directory (password policy)

**Discovery questions:**
- What recovery factors are acceptable (security question, email, SMS, Okta Verify)?
- Are there password complexity/rotation requirements mandated by compliance (and is FastPass reducing password reliance over time)?
- What is the helpdesk fallback process when self-service recovery fails?
- Are there user populations without reliable recovery factor coverage (e.g., shared devices, no personal phone)?

### Conditional/Contextual Access (Device, Network, Risk)

**Typical flow:**
Sign-in attempt → Device Assurance Policy evaluated (OS version, encryption, patch level) → Network Zone checked → Risk score/behavior evaluated → Access granted, challenged, or denied per Authentication Policy rule

**Key Okta components:** Device Assurance Policies, Network Zones, Authentication Policies, Okta ThreatInsight, Adaptive MFA

**Discovery questions:**
- What device posture signals matter most (managed vs. unmanaged, encryption, OS patch currency)?
- Is there an existing MDM/EMM or endpoint security tool whose signals should factor into policy?
- Should unmanaged/BYOD devices be blocked outright, granted limited access, or just challenged harder?
- What network locations are considered trusted, and how are they defined (corporate egress IPs, VPN)?
- Is there a need to distinguish "risk" (ThreatInsight, behavior anomalies) from "posture" (device assurance) in the same policy, or should they be layered separately?

---

## Honest Capability Assessment

When creating implementation guides, be accurate about what WIC can and cannot do natively. Do not overstate capabilities.

### Strengths (lean into these)
- Deep OIN catalog (thousands of pre-built integrations) accelerates SaaS SSO rollout without custom integration work
- FastPass delivers genuine phishing-resistant passwordless authentication, not just a marketing label — it uses device-bound public key cryptography
- Authentication Policies and Global Session Policy give fine-grained, layered control without custom code
- Okta Workflows extends automation to apps and processes outside native provisioning support, no separate iPaaS license required for most workforce scenarios
- Device Assurance Policies natively evaluate OS version, encryption, and patch state without requiring a third-party MDM integration (though they integrate with MDM/EMM signals when available)
- ThreatInsight provides cross-tenant threat intelligence "for free" as part of the platform, not a bolt-on

### Gaps to Acknowledge (document as discovery items)
- **Legacy/on-prem app support**: Apps using header-based auth, Kerberos, or other pre-modern protocols need Okta Access Gateway (a separate deployment) or a custom reverse-proxy pattern — not solved by SSO alone
- **FastPass platform/browser coverage**: FastPass support varies by OS version and browser; older OS builds or unsupported browsers fall back to weaker factors, and this needs explicit validation against the customer's fleet
- **Device Assurance depth without MDM**: Native device signals (OS version, encryption, screen lock) are useful but shallower than full MDM-sourced posture data (e.g., jailbreak detection nuance, app inventory) — pairing with an existing MDM/EMM is recommended for higher-assurance requirements
- **Workflows scaling/governance**: Okta Workflows is powerful but flows are built and maintained per-org; there's no built-in flow versioning/CI-CD equivalent to mature iPaaS tooling, so complex flow libraries need internal governance discipline
- **Risk scoring depth**: ThreatInsight and Behavior Detection Rules provide useful signals but are not a full UEBA/risk-scoring engine — organizations needing sophisticated continuous risk scoring often pair Okta with a dedicated ITDR/SIEM tool
- **API Access Management is a separate add-on**: Custom authorization servers for first-party API protection are not included in base WIC editions and require the API Access Management add-on (except in Integrator Free Plan orgs, which get one default authorization server)

Frame gaps as discovery items: "Validate whether [capability] meets the customer's specific requirements, or if augmentation via Workflows/MDM integration/a dedicated tool is needed."

---

## Diagram Component Mapping

When creating Mermaid diagrams for Okta WIC, use these class assignments:

| Okta Component | Mermaid Class |
|---------------|---------------|
| HR system, AD/LDAP, external IdPs, end user sign-in action | `trigger` or `extSystem` |
| Universal Directory, Identity Engine core, Global Session Policy | `platform` |
| Okta Workflows | `workflow` |
| Authentication Policy evaluation, Device Assurance checks, risk/policy decisions | `decision` |
| Adaptive MFA policy, Access Certifications (when referenced from OIG) | `governance` |
| SSO assertion issuance, SCIM provisioning, app assignment | `action` |
| Access granted, session established, account active | `endpoint` |
| Access denied, sign-in blocked, ThreatInsight block | `danger` |
| System log entry, sign-in audit trail | `audit` |
| Push notification, recovery email/SMS | `notify` |
