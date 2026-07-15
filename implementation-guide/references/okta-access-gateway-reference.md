# Okta Access Gateway (OAG) Reference

## Platform Components

Use these component names consistently across all documents. Map use cases to the appropriate components.

### Core Access Gateway Components

| Component | What It Does | Common Use Cases |
|-----------|-------------|------------------|
| **Okta Access Gateway (OAG)** | Self-hosted reverse-proxy virtual appliance that extends Okta SSO/MFA to on-prem legacy web apps that cannot speak SAML/OIDC natively | Legacy WAM replacement, on-prem app modernization bridge |
| **Admin Node** | Appliance node running the OAG management console/configuration | Central configuration of apps, policies, cluster settings |
| **Worker Node(s) / Cluster** | Appliance node(s) that handle live proxy traffic between users and backend apps | Request routing, header injection, session handling at scale |
| **Header-Based SSO (Generic Header app)** | Injects user attributes as HTTP headers on requests to the backend app | Legacy apps built for header-based/WAM-style auth (e.g., prior SiteMinder, IIS) |
| **Kerberos / Integrated Windows Auth (IWA) Constrained Delegation** | OAG obtains a Kerberos ticket on the user's behalf and presents it to the backend app | Windows-authenticated intranet apps (IIS/IWA), AD-integrated line-of-business apps |
| **SAML Pass-Through** | Forwards the SAML assertion Okta issued at login through to the backend app rather than minting a new one | Legacy apps expecting to consume Okta's original SAML assertion |
| **Application Policies** | Per-app access rules: Protected, Not Protected, Protected Rule (attribute/group match), Adaptive, Custom (nginx-level) | Restricting app access by group/attribute, custom edge-case logic |
| **Attribute/Claim Mapping** | Maps Universal Directory fields to outbound headers, cookies, or Kerberos principal | Passing username, email, roles, or entitlements to the legacy app |

### Supporting Components

| Component | What It Does |
|-----------|-------------|
| **Load Balancer (customer-provided)** | Distributes traffic across OAG worker nodes; required for HA, needs session affinity (sticky sessions) |
| **Active Directory / KDC** | Domain controller used for Kerberos constrained delegation; requires a dedicated service account and keytab |
| **Okta (as IdP)** | Authenticates the user and establishes the session OAG validates before proxying to the backend app |
| **Universal Directory (UD)** | Source of user attributes used in header/claim mapping |
| **Hypervisor / Cloud Platform** | OAG ships as an OVA; supported targets include VMware vSphere/ESXi, and CLI-driven deployment paths for AWS, Azure, GCP, OCI, and Nutanix |
| **Capacity Tiers (PoC / Small / Medium / Large)** | Okta-published sizing guidance for worker-node count and app count per cluster |

### Important Distinctions

**Header-Based SSO vs Kerberos/IWA vs SAML Pass-Through**
- These are three separate authentication-injection modes configured per app, not interchangeable settings. Header-based SSO suits apps built for WAM-style header trust. Kerberos/IWA suits Windows-authenticated apps on AD-joined servers. SAML pass-through forwards Okta's original assertion — it is **not** OAG minting a fresh SAML response, so validate that the backend app can actually consume Okta's assertion as-is before assuming this path works.
- Pick the mode based on what the legacy app already expects, not what's easiest to configure in Okta.

**OAG Appliance vs Modern OIN App SSO**
- If an application already supports SAML or OIDC (directly, or via an existing Okta Integration Network entry), use standard Okta SSO — do not route it through OAG. OAG exists specifically for apps that **cannot** speak modern federation protocols.
- Onboarding an app to OAG that could instead be federated directly adds unnecessary appliance infrastructure and maintenance burden.

**OAG vs Okta Privileged Access (OPA) / Advanced Server Access**
- These are different products solving different problems. OAG is a reverse proxy for **web application** traffic (HTTP/HTTPS). OPA/Advanced Server Access governs **SSH/RDP access to servers**. Don't conflate a request to "put SSO in front of a legacy web app" with a request to "manage privileged server access" — they route to different Okta products and different implementation guides.

**Kerberos Delegation Site Limitation**
- OAG's Kerberos constrained delegation is documented as limited to one app per IIS default site. Multiple IWA apps behind the same IIS server may require additional site bindings — confirm this during technical design, not after cutover.

---

## Common Access Gateway Use Case Patterns

### SSO to On-Prem Legacy Web Apps via Header Injection

**Typical flow:**
User authenticates to Okta → Okta session established → user requests app URL → OAG worker node intercepts request and validates Okta session → OAG injects mapped user attributes as HTTP headers → backend app trusts headers and grants access

**Key Okta components:** Okta Access Gateway (Generic Header app type), Universal Directory, Attribute/Claim Mapping, Application Policies

**Discovery questions:**
- Does the legacy app already trust upstream headers for authentication (existing WAM/SiteMinder/header-based SSO today)?
- What specific attributes does the app expect in headers (username, email, roles, entitlements), and in what header names/format?
- Is authentication required on every request, or does the app rely on its own session cookie after the first hit?
- Can OAG worker nodes reach the app's backend network path (firewalls, VPC peering, DNS)?
- Is there an existing WAM system being replaced, and what is the cutover plan?

### Kerberos-Based SSO to IWA Apps

**Typical flow:**
User authenticates to Okta → OAG validates session → OAG requests a Kerberos ticket via constrained delegation → OAG presents the ticket to the backend IIS/IWA app → app validates against Active Directory → access granted

**Key Okta components:** Okta Access Gateway (Kerberos Constrained Delegation app type), Active Directory (KDC, dedicated service account, keytab), Application Policies

**Discovery questions:**
- Is Active Directory reachable from the OAG deployment, and is there an existing (or plannable) AD trust path?
- Has a dedicated AD service account with constrained delegation rights been provisioned for OAG?
- Is the backend app hosted on IIS as the default site, or will the one-app-per-default-site limitation require additional planning?
- What is the app's current auth method (NTLM, Kerberos passthrough, IWA browser prompt) today?
- Are there multiple IWA apps that will need separate site bindings or dedicated OAG app configs?

### Protecting Legacy Apps with Modern MFA

**Typical flow:**
User requests legacy app → Okta sign-on policy enforces MFA at login → Okta session established → OAG validates session → Application Policy evaluated (Protected / Protected Rule / Adaptive) → access granted or denied

**Key Okta components:** Okta Sign-On Policies (MFA/Adaptive), Okta Access Gateway Application Policies, Universal Directory

**Discovery questions:**
- Does the legacy app have any native MFA today, or is it currently single-factor/password-only?
- What conditions should trigger step-up (network zone, device trust, risk signal)? Confirm whether that logic should live in the Okta org sign-on policy or an OAG Application Policy — this needs to be validated per environment, as native IP allow-list/step-up conditions inside OAG policy itself are not consistently documented.
- Which user populations/groups should be granted vs explicitly blocked (Protected Rule logic)?
- Is custom policy logic needed beyond the standard policy types (Custom/nginx-level rules)?

### Hybrid Access (On-Prem + Cloud) Under One IdP

**Typical flow:**
User authenticates once to Okta → accesses a mix of cloud apps via native SAML/OIDC (OIN) and on-prem legacy apps via OAG → single dashboard, single session, consistent MFA policy across both

**Key Okta components:** Okta (as IdP), Okta Integration Network (OIN), Okta Access Gateway, Universal Directory

**Discovery questions:**
- Which apps are genuine OAG candidates vs which already support modern federation and should bypass OAG entirely?
- Is OAG intended as a long-term access layer, or an interim bridge while legacy apps are modernized/retired?
- What is the roadmap and timeline for retiring the legacy apps currently fronted by OAG?
- Are there multiple on-prem sites/networks that will require separate OAG clusters rather than one shared cluster?
- What operational ownership exists for the OAG appliance itself (patching, HA, DR, monitoring) — is this the customer's infra team or a managed service?

---

## Honest Capability Assessment

When creating implementation guides, be accurate about what Okta Access Gateway can and cannot do natively. Do not overstate capabilities.

### OAG Strengths (lean into these)
- Extends Okta SSO/MFA to legacy web apps that cannot speak SAML/OIDC, without requiring code changes to the app
- Reverse-proxy architecture centralizes authentication in front of many legacy apps at once
- Multiple auth-injection modes (header, Kerberos/IWA, SAML pass-through, cookie) cover the common legacy WAM patterns
- Clustered worker-node deployment supports horizontal scaling and high availability
- Explicitly positioned by Okta as a WAM modernization/migration bridge, letting customers retire legacy access-management infrastructure at their own pace

### OAG Gaps to Acknowledge (document as discovery items, not limitations)
- **Appliance infrastructure burden**: OAG is a self-hosted OVA, not a SaaS service — the customer owns provisioning, patching, OS/network configuration, and load balancer setup for the cluster
- **HTTP(S)-only**: Access Gateway proxies web traffic; it does not extend to thick-client apps or non-HTTP(S) protocols
- **SAML pass-through nuance**: OAG forwards Okta's original assertion rather than issuing a fresh SAML response tailored to the backend app — validate the target app's actual assertion requirements before assuming this path fits
- **Kerberos delegation scope**: constrained delegation is documented as limited to one app per IIS default site; multiple IWA apps may require additional planning
- **WS-Federation and native credential-injection (Basic Auth/form-fill)**: not clearly documented as supported app types as of current release notes — validate directly against the current OAG app-type catalog before designing a solution around them
- **Policy condition placement**: native IP allow-list/step-up MFA conditions inside OAG Application Policy are not consistently documented; this logic may need to live in Okta's org-level sign-on policy instead
- **Identity Engine dependency**: whether OAG requires Okta Identity Engine (vs Classic) is not clearly documented publicly — confirm against the customer's specific org type during design
- **Licensing model**: per-app/per-user/per-node licensing is not published; confirm current terms with the account team
- **Migration-bridge positioning**: OAG is marketed as a bridge, not a permanent target-state architecture — plan for eventual app modernization/retirement rather than treating OAG as the end state

Frame gaps as discovery items: "Validate whether [capability] meets the customer's specific requirements, or if the app should instead be scoped for direct modern federation once feasible."

---

## Diagram Component Mapping

When creating Mermaid diagrams for Okta Access Gateway, use these class assignments:

| Okta Component | Mermaid Class |
|---------------|---------------|
| User access request, scheduled health check | `trigger` |
| Legacy on-prem app, Active Directory/KDC, external network | `extSystem` |
| Okta (IdP), Universal Directory | `platform` |
| Okta Workflows (custom automation alongside OAG, e.g. cert rotation alerts) | `workflow` |
| Application Policy evaluation (Protected, Protected Rule, Adaptive, Custom) | `decision` |
| Okta sign-on policy, MFA/step-up enforcement | `governance` |
| OAG worker node processing, header injection, Kerberos ticket issuance, SAML pass-through | `action` |
| Access granted, session established | `endpoint` |
| Access denied, policy blocked | `danger` |
| OAG/Okta System Log | `audit` |
| Email/Slack alerts (HA failover, cluster health, cert expiry) | `notify` |
