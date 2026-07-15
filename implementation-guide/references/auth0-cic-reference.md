# Customer Identity Cloud (powered by Auth0) Reference

## Platform Components

Use these component names consistently across all documents. Map use cases to the appropriate components. Both product names resolve to the same platform: **Okta Customer Identity Cloud (CIC)** is the enterprise/flagship product name; **Auth0 by Okta** is the name developers see in the dashboard, docs, code, and APIs. Use "Customer Identity Cloud (powered by Auth0)" on first reference in customer-facing docs, then "Auth0" or "CIC" thereafter.

### Core Components

| Component | What It Does | Common Use Cases |
|-----------|-------------|------------------|
| **Universal Login** | Centralized, hosted authentication experience (login, signup, password reset) shared across all apps in a tenant | Consistent branded login across web/mobile/SPA, reducing custom auth-UI maintenance |
| **Connections** | Configured identity sources a tenant can authenticate against — Database, Social, Enterprise (SAML/OIDC/AD/Azure AD), Passwordless | Username/password auth, social login, enterprise SSO federation, OTP/magic-link login |
| **Actions** | Current extensibility model — custom Node.js code that runs at defined points in a flow (triggers: post-login, pre-user-registration, M2M token issuance, password reset, send phone message, etc.) | Custom claims, MFA step-up logic, external API enrichment, progressive profiling, custom notifications |
| **Forms** | No-code visual editor for building custom steps into login/signup flows | Progressive profiling, policy/consent acceptance, OTP verification steps, third-party data collection (e.g., Stripe) |
| **Organizations** | B2B multi-tenancy construct — model business customers as Organizations within a single Auth0 tenant, each with its own membership, branding, and connections | SaaS apps serving multiple business customers from one tenant; org-specific SSO and branding |
| **Machine-to-Machine (M2M) Applications** | Application type using the OAuth2 Client Credentials grant to obtain access tokens for service-to-service calls (no user present) | Backend services, CLIs, daemons calling a protected API |
| **Attack Protection** | Bundle of automated threat-mitigation signals: Bot Detection, Brute-Force Protection, Breached Password Detection, Suspicious IP Throttling | Credential-stuffing mitigation, automated bot/script blocking, compromised-credential blocking |
| **Adaptive MFA** | Risk-based step-up authentication that varies MFA challenges based on contextual signals (new device, location, IP reputation) | Reducing MFA friction for low-risk logins while enforcing it for high-risk ones |
| **RBAC (Roles & Permissions)** | Role-based access control defined on API resource servers; roles bundle permissions, permissions appear as scopes in access tokens | Authorizing API calls by role rather than per-user scope assignment |

### Supporting Components

| Component | What It Does |
|-----------|-------------|
| **Branding & Custom Domains** | Tenant-level and Organization-level branding (logo, colors, custom HTML) for Universal Login; custom domain support so login pages appear under the customer's own domain instead of `*.auth0.com` |
| **Management API** | REST API for administering tenant configuration (users, connections, applications, rules/actions, organizations) — the API underlying the Dashboard and most Terraform/IaC providers |
| **Tenants** | The top-level isolation boundary in Auth0 (`tenant.region.auth0.com`); most implementations use separate tenants per environment (dev/staging/prod) |
| **Rules (legacy)** | Deprecated pre-Actions extensibility model limited to post-authentication customization | Do not recommend for new builds |
| **Hooks (legacy)** | Deprecated pre-Actions extensibility model for specific extension points (pre/post user registration, password change) | Do not recommend for new builds |
| **Auth0 Fine-Grained Authorization (FGA)** | Separate, Zanzibar-inspired relationship-based authorization service for modeling fine-grained/ReBAC permissions at the object level | Has its own dedicated reference file — see `auth0-fga-reference.md`. Do not cover FGA modeling in depth here; cross-reference instead. |

### Important Distinctions

**Actions vs legacy Rules/Hooks**
- **Actions** is the current, actively developed extensibility model and the only one recommended for new implementations. Rules and Hooks are legacy: as of November 18, 2024 they are closed to new tenants and can no longer be edited (only toggled on/off); Auth0 will stop executing them entirely after November 18, 2026.
- Any existing customer still on Rules/Hooks should be flagged as a migration item during discovery, not treated as a stable long-term state.

**Organizations vs separate tenants**
- **Organizations** models multiple business customers *within a single tenant* — one Auth0 tenant, many Organizations, each with its own membership/branding/connections. This is the standard pattern for B2B SaaS multi-tenancy.
- **Separate tenants** is a heavier-weight isolation boundary (different tenant domains, fully separate configuration) typically reserved for environment separation (dev/staging/prod) or hard regulatory/data-residency isolation — not for every business customer.
- Don't default to "one tenant per customer" when Organizations solves the requirement with far less operational overhead.

**Customer Identity Cloud vs Auth0 by Okta vs Okta Workforce Identity**
- "Okta Customer Identity Cloud" and "Auth0 by Okta" are marketing names for the *same underlying platform and APIs* — no URLs, APIs, or code libraries differ between them. Use CIC in customer-facing/enterprise materials; expect "Auth0" terminology in the Dashboard, docs, SDKs, and Management API.
- This is a **distinct product** from Okta Workforce Identity Cloud (the employee/B2E IAM and OIG platform documented in `okta-oig-reference.md`). CIC/Auth0 is purpose-built for consumer (B2C) and business-customer (B2B) identity — it does not include Workforce Identity concepts like Lifecycle Management, Access Certifications, or HR-driven joiner/mover/leaver automation. If a customer needs both employee and customer identity, expect two separate implementations (Workforce Identity + CIC), not one.

---

## Common Customer Identity Use Case Patterns

### Consumer Signup & Login

**Typical flow:**
User hits app → Redirect to Universal Login → Database Connection presents signup/login form → Credentials validated → (Optional) Actions trigger for custom claims/enrichment → Token issued → Redirect back to app

**Key components:** Universal Login, Database Connection, Actions (post-login trigger), Attack Protection

**Discovery questions:**
- Will Auth0 be the source of truth for user credentials, or does an existing user store need to be imported/federated?
- What custom user profile attributes need to be captured at signup?
- What password policy and account verification (email/phone) requirements exist?
- Does the login experience need to be embedded (Lock/SDK) rather than redirect-based, and is that acceptable given Universal Login's security/maintenance advantages?
- What Attack Protection thresholds are appropriate for expected traffic volume (to avoid false positives at scale)?

### Social Login

**Typical flow:**
User selects social provider on Universal Login → Redirect to provider (Google, Facebook, Apple, etc.) → Provider authenticates and returns profile → Auth0 creates/links user → Actions trigger for profile normalization → Token issued

**Key components:** Social Connections, Actions (account linking/normalization), Universal Login

**Discovery questions:**
- Which social providers are required, and does the customer have (or need to create) developer app registrations with each provider?
- How should accounts be linked if a user signs up via social after previously registering with a database connection (same email)?
- What profile data is needed from each provider, and do scopes/consent screens need customization?
- Are there providers requiring approval or extended verification (e.g., Apple, Facebook business verification) that affect timeline?

### B2B Multi-Tenant with Organizations

**Typical flow:**
User accesses app → Organization identified (by invite link, email-domain discovery, or org-picker prompt) → Org-specific branding/connection applied → User authenticates (possibly via org's own enterprise SSO) → Org membership and roles included in token → App scopes access by organization

**Key components:** Organizations, Enterprise Connections, RBAC, Branding & Custom Domains, Actions (org-specific claims)

**Discovery questions:**
- How will users be mapped to an Organization — invitation flow, email-domain matching, or manual assignment?
- Do individual business customers require their own SSO (SAML/OIDC) federation, or is Auth0-hosted login sufficient for all orgs?
- Does each Organization need distinct branding, or is shared branding acceptable?
- How many Organizations are expected, and does membership/role structure vary significantly between them?
- Should users be able to belong to multiple Organizations simultaneously?

### Passwordless Authentication

**Typical flow:**
User enters email/phone on Universal Login → Passwordless Connection sends OTP/magic link → User submits code or clicks link → Auth0 validates and issues token

**Key components:** Passwordless Connection, Universal Login, Actions (for fallback/step-up logic)

**Discovery questions:**
- Email OTP, SMS OTP, or magic link — which channel(s), and is there an existing SMS/email delivery provider to integrate?
- What is the fallback if a user cannot receive the OTP/link (delivery failure, spam filtering)?
- Are there cost implications from SMS delivery volume the customer should plan for?
- Should passwordless coexist with password-based login, or fully replace it?

### M2M / API Authorization

**Typical flow:**
Backend service authenticates with Client ID/Secret → Client Credentials grant issued against target API (resource server) → Access token includes authorized scopes/permissions → Service calls protected API

**Key components:** M2M Applications, Client Credentials Grant, RBAC (Roles & Permissions on the resource server), Management API (for service-to-service admin automation)

**Discovery questions:**
- What backend services need to call which APIs, and what is the least-privilege scope set for each?
- Is client secret rotation/storage handled via a secrets manager, or does the implementation need guidance on that?
- Does any M2M application need to call the Auth0 Management API itself (e.g., automated user provisioning), which requires its own dedicated M2M app and scopes?
- What are the token lifetime and rate-limit requirements for expected M2M call volume?

### Attack Protection & Bot Mitigation

**Typical flow:**
Login/signup/password-reset request received → Attack Protection signals evaluated (bot score, IP reputation, breached-credential match, failed-attempt velocity) → Allow, challenge (CAPTCHA/MFA), or block → Notification sent if applicable

**Key components:** Attack Protection (Bot Detection, Brute-Force Protection, Breached Password Detection, Suspicious IP Throttling), Adaptive MFA, Actions (custom response logic)

**Discovery questions:**
- What is acceptable user friction (CAPTCHA prompts, temporary blocks) versus risk tolerance for the customer's traffic profile?
- Does the customer need custom blocking/notification logic beyond Auth0's default thresholds (via Actions)?
- Are there known high-volume legitimate traffic patterns (e.g., bulk corporate logins from one IP) that could trigger false positives and need allowlisting?
- What user notification is expected when brute-force or breached-password protection triggers (email, in-app message)?

### Progressive Profiling / Account Linking

**Typical flow:**
User authenticates with minimal initial profile → Actions/Forms evaluate profile completeness or business rule → Additional data collection step presented (Form) → Profile updated → Separate identities linked (if same person authenticates via multiple connections) → Token issued with consolidated profile

**Key components:** Forms, Actions, Account Linking (via Management API/Actions), Universal Login

**Discovery questions:**
- What attributes are mandatory at signup versus deferred to progressive profiling, and what triggers the deferred prompt (login count, time since signup, specific app feature access)?
- How should identity linking be handled when the same person authenticates via different connections (e.g., database + Google) with the same email — automatic, prompted, or manual admin process?
- Where does the consolidated profile live — Auth0 user profile metadata, or synced to an external system of record?
- Are there compliance/consent requirements (e.g., re-consent to updated terms) that should be enforced via a Forms step?

---

## Honest Capability Assessment

When creating implementation guides, be accurate about what Customer Identity Cloud (Auth0) can and cannot do natively. Do not overstate capabilities.

### Strengths (lean into these)
- Universal Login provides a mature, centrally-managed, brandable authentication surface with WCAG 2.2 AA-audited accessibility
- Broad out-of-the-box Connection support (database, social, enterprise SAML/OIDC/AD, passwordless) without custom protocol code
- Actions provide flexible, code-level extensibility at well-defined trigger points without needing a separate middleware layer
- Organizations give B2B SaaS a native multi-tenant model without provisioning a tenant per customer
- Attack Protection and Adaptive MFA are built in and require no separate security vendor integration for baseline threat mitigation
- Forms enables no-code custom flow steps (progressive profiling, consent) without a full custom UI build
- Management API and mature Terraform/Deploy CLI support enable configuration-as-code for CI/CD-driven tenant management

### Gaps to Acknowledge (document as discovery items, not limitations)
- **Rules/Hooks sunset**: Any environment still relying on Rules or Hooks needs an Actions migration plan; these are closed to edits for new logic and stop executing entirely after November 18, 2026
- **Fine-grained/relationship-based authorization**: RBAC here is role/permission-based at the API scope level; true object-level or relationship-based authorization (e.g., "user X can edit document Y because they're a member of team Z") requires Auth0 FGA, a separate product — do not assume base CIC/Auth0 RBAC covers this
- **Cross-tenant reporting/analytics**: Auth0's built-in analytics and logs are tenant-scoped; consolidated reporting across many tenants/Organizations at enterprise scale typically requires log streaming to an external SIEM/BI tool
- **Identity correlation across pre-existing user stores**: Migrating or federating a large legacy user base (password hash compatibility, custom DB connection scripts) is a real engineering effort, not a config toggle — flag early in discovery
- **Workforce Identity Governance features are out of scope**: OIG capabilities (access certifications, entitlement management, lifecycle joiner/mover/leaver) documented in `okta-oig-reference.md` do not exist in CIC/Auth0; if a use case blends consumer identity with employee governance, expect two platforms and an integration point between them
- **Custom Domain setup has real prerequisites**: Custom domains require DNS control and (for some configurations) additional TLS certificate management — this is an infrastructure dependency, not a pure Auth0 setting

Frame gaps as discovery items: "Validate whether [capability] meets the customer's specific requirements, or if augmentation via Actions/FGA/an external system is needed."

---

## Diagram Component Mapping

When creating Mermaid diagrams for Customer Identity Cloud (Auth0), use these class assignments from `mermaid-standards.md` — do not invent new classes.

| CIC/Auth0 Component | Mermaid Class |
|---------------|---------------|
| User-initiated login/signup, scheduled token expiry | `trigger` |
| Social/Enterprise IdP, external SMS/email provider, external API called by M2M app | `extSystem` |
| Universal Login, Connections, Organizations resolution, Auth0 core auth pipeline | `platform` |
| Actions (custom logic execution), Forms flow steps | `workflow` |
| Attack Protection evaluation, Adaptive MFA risk check, RBAC/permission check | `decision` |
| RBAC role/permission assignment, Organization membership rules | `governance` |
| Token issuance, account linking, profile update, M2M scope grant | `action` |
| Login complete / token returned to app | `endpoint` |
| Access denied, account blocked (brute-force/bot block) | `danger` |
| Auth0 Logs, log streaming to SIEM | `audit` |
| Email/SMS OTP delivery, breach/brute-force user notification | `notify` |
