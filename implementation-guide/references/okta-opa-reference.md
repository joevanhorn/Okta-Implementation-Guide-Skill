# Okta Privileged Access (OPA) Reference

## Platform Components

Use these component names consistently across all documents. Map use cases to the appropriate components.

### Core Privileged Access Components

| Component | What It Does | Common Use Cases |
|-----------|-------------|------------------|
| **Okta Privileged Access (OPA)** | Umbrella PAM product for securing, managing, and monitoring access to servers and infrastructure (evolution of Advanced Server Access / ASA) | All privileged access use cases |
| **Resource Groups** | Top-level administrative boundary; owned by delegated resource admins who manage the projects within them | Delegating PAM administration by team, business unit, or environment |
| **Projects** | Container for enrolled servers within a Resource Group; scopes which Security Policies and CA certificates apply | Grouping servers by application, environment (prod/non-prod), or compliance tier |
| **Server Agent & Enrollment** | Software installed on each Linux/Windows server; enrolls into a Project via an enrollment token and mints local users on demand | Bringing a server under OPA management |
| **Gateways** | Network intermediary that brokers SSH/RDP connections so the client never holds credentials usable to connect directly | Routing access through segmented networks, enabling session recording, RDP access |
| **Security Policies** | Rule engine defining which user groups can access which resources, via which methods (SSH, RDP, sudo, checkout), under what conditions | Access control, approval requirements, method restrictions |
| **Sudo Command Bundles** | Allow-listed sets of Linux commands (max 64 per bundle) referenced inside a Security Policy to scope root-equivalent access | Granular sudo control instead of blanket root |
| **Password & Secret Checkout** | Secrets Vault storing passwords, API keys, and other credentials; enforces one-user-at-a-time checkout for a bounded duration | Shared/service account access, legacy systems that can't use certificates |
| **Active Directory Accounts** | AD Agent-based discovery and management of domain accounts for SSH/RDP sign-in | Domain-joined server access, AD credential rotation |
| **Session Recording (Session Capture)** | Records and signs SSH/RDP sessions for tamper-evident audit trails | Compliance audit, training, incident investigation |
| **Ephemeral Certificates** | Short-lived client certificates (default 3-minute expiry) minted by the Project CA per connection; the basis for zero standing privilege | Eliminating static SSH keys and passwords |

### Supporting Components

| Component | What It Does |
|-----------|-------------|
| **Okta Privileged Access Client** | End-user application/CLI used to authenticate and initiate connections |
| **Delegated Resource Admins** | Owners of a Resource Group who manage its Projects without central PAM team involvement |
| **Service Accounts (Okta & SaaS)** | Centralized management of non-federated SaaS and platform service identities |
| **Workload Identity** | Certificate-based identity for automation/service-to-service connections, replacing static keys in scripts and pipelines |
| **RDP Transcoder** | Converts raw `.asa` binary RDP session logs into reviewable `.mkv` video |
| **Access Requests (via OIG integration)** | Optional approval condition inside a Security Policy that routes elevation through Okta Identity Governance |

### Important Distinctions

**Ephemeral Certificate Access ≠ Password/Secret Checkout**
- **Ephemeral certificates**: Zero standing privilege. A short-lived client certificate (default 3 minutes) is minted per connection and self-expires — nothing to rotate or clean up. This is the default, preferred model for individual server/database sign-in.
- **Password/Secret Checkout**: For shared or service accounts that cannot use certificate-based sign-in (legacy systems, break-glass accounts, third-party SaaS service accounts). Enforces one-user-at-a-time exclusivity for a defined checkout window rather than eliminating the standing credential.
- Use ephemeral certs wherever possible; reserve checkout for accounts that genuinely can't be converted.

**OPA ≠ OIG (Okta Identity Governance)**
- **OPA** operates at the infrastructure layer: server sign-in, certificates, sudo, secrets, session recording.
- **OIG** operates at the application/entitlement governance layer: access requests, approvals, certifications.
- They integrate, but OPA does not replace OIG: group membership requests and approvals are **not** available natively inside OPA. If the customer needs a request/approval workflow for privileged group membership, that dependency runs through OIG Access Requests, not OPA alone.

**Security Policy ≠ Sudo Command Bundle**
- **Security Policy**: The rule engine — defines principals (user groups), resource selectors, and privileges (SSH, RDP, sudo, checkout) and any required conditions (MFA, Access Requests).
- **Sudo Command Bundle**: A specific privilege object — an allow-listed set of Linux commands. A bundle by itself grants nothing; it must be referenced inside a Security Policy rule to take effect.

**Resource Group ≠ Project**
- **Resource Group**: The ownership/administration boundary, assigned to delegated resource admins.
- **Project**: The operational unit inside a Resource Group — the actual pool of enrolled servers and the scope at which Security Policies and the backing CA apply. One Resource Group can contain multiple Projects.

---

## Common Privileged Access Use Case Patterns

### Privileged Server Access (SSH/RDP) with Ephemeral Credentials

**Typical flow:**
User opens OPA client → Okta SSO/MFA authentication → device posture check → connection request to a server in a Project → Security Policy evaluated → Project CA mints a short-lived client certificate (default 3 min) → connection established directly or via Gateway (required for RDP) → certificate self-expires at session end

**Key Okta components:** OPA Client, Security Policies, Server Agent, Projects (CA), Gateways (for RDP), Okta MFA/Device Trust

**Discovery questions:**
- Which OS/platforms and versions need coverage (Linux distros, Windows Server versions)?
- Is direct client-to-server SSH acceptable, or does network segmentation require routing through a Gateway?
- What device trust and MFA requirements must be satisfied before a connection is authorized?
- Do users need root/administrator-level access, or scoped principal accounts?
- What bastion hosts or jump servers is this expected to replace?

### Password/Secret Checkout for Shared Accounts

**Typical flow:**
Shared or service account credential stored in the Secrets Vault → user requests checkout → Security Policy evaluates group membership/approval → credential revealed for a defined checkout window (one user at a time) → admin can force check-in → checkout event logged

**Key Okta components:** Password & Secret Checkout, Security Policies, Active Directory Accounts (for domain-based checkout), Resource Groups/Projects (checkout settings)

**Discovery questions:**
- Which shared/service accounts currently lack individual attribution (root, `sa`, service accounts)?
- What checkout duration is acceptable, and should the credential rotate automatically after check-in?
- Are these local accounts, AD accounts, or SaaS app service accounts?
- Who needs visibility into which accounts are checked out and by whom, at any given time?
- Should checkout require an explicit approval step, or is group membership sufficient?

### Just-in-Time Privilege Elevation

**Typical flow:**
User has no standing access → requests access to a Project/resource (optionally routed through OIG Access Requests) → approval workflow completes → Security Policy grants time-bound privileges → ephemeral certificate issued for the approved window → access expires automatically, no manual revocation required

**Key Okta components:** Security Policies (Access Requests condition), Okta Identity Governance integration, Ephemeral Certificates, Resource Groups/Projects

**Discovery questions:**
- Is standing (always-on) access acceptable for any user tier, or is JIT required across the board?
- Should elevation approvals route through OIG Access Requests, or is group-based always-on access sufficient for lower-risk tiers?
- What is the maximum access window once elevation is approved?
- How should emergency/break-glass access be handled when approvers are unavailable?
- Does the customer already run OIG, or does this pattern introduce it as a new dependency?

### Sudo Command Control on Linux

**Typical flow:**
Admin defines a Sudo Command Bundle (allow-listed commands, max 64 per bundle) → bundle referenced in a Security Policy rule for a user group → user connects via SSH → policy grants sudo-level access scoped to bundle commands only → command execution logged

**Key Okta components:** Sudo Command Bundles, Security Policies, Server Agent (Linux), Session Recording

**Discovery questions:**
- What specific commands do different user tiers actually need (service restart, log viewing, package management)?
- Should any group retain full root-equivalent sudo, or is command-scoped access required for all non-admin tiers?
- Who owns bundle maintenance as application and server needs evolve?
- Do specific commands need argument restrictions (any, none, or specific arguments only)?

### Session Recording & Audit for Compliance

**Typical flow:**
Session capture enabled at the Project/policy level → SSH/RDP session routed through a Gateway → session recorded and cryptographically signed → logs stored locally on the gateway or shipped to S3/GCS → RDP sessions converted via the transcoder to reviewable `.mkv` video → compliance team retrieves and reviews recordings on demand

**Key Okta components:** Gateways, Session Recording, RDP Transcoder, Resource Groups/Projects (capture settings), Okta System Log

**Discovery questions:**
- What compliance framework drives the recording requirement (PCI DSS, SOC 2, FedRAMP, etc.), and what retention period does it mandate?
- Where should finalized session logs be stored (local gateway storage vs. S3/GCS), and who owns that storage lifecycle?
- Should recording apply to all privileged sessions, or only specific Projects/tiers?
- Who needs access to review recordings, and what is the process for producing a video from raw logs?
- Are RDP sessions in scope, requiring Gateway and transcoder deployment in addition to SSH coverage?

---

## Honest Capability Assessment

When creating implementation guides, be accurate about what OPA can and cannot do natively. Do not overstate capabilities.

### OPA Strengths (lean into these)
- Zero standing privilege via short-lived ephemeral certificates (default 3-minute expiry), eliminating long-lived SSH keys and static passwords
- Native integration with Okta SSO, MFA, and device trust — privileged sessions authenticate through the same identity plane as everything else, not a separate silo
- Delegated resource administration lets infrastructure teams own their Resource Groups/Projects without funneling every change through a central PAM team
- Signed, tamper-evident session recording for both SSH and RDP
- Sudo Command Bundles enable granular, auditable Linux privilege scoping instead of blanket root access
- Secrets Vault centralizes checkout of shared/service credentials with one-user-at-a-time exclusivity and forced check-in

### OPA Gaps to Acknowledge (document as discovery items, not limitations)
- **PAM maturity vs. incumbents**: OPA is materially younger and narrower than dedicated PAM platforms like CyberArk, BeyondTrust, or Delinea. Session isolation and vaulting depth lag those platforms. Treat OPA as an emerging capability for large or complex privileged-access programs, not an automatic drop-in replacement for an established PAM tool.
- **Target coverage is server-centric**: Native strength is Linux/Windows servers and AD domain accounts. Coverage for network devices (routers, switches, firewalls), mainframes, and database-native privileged sessions is comparatively limited next to legacy PAM tools built around those targets — validate specific target-system coverage during discovery.
- **Configuration scale limits exist**: Per Okta's published limits, teams are capped at 250 Security Policies (30 rules per policy, 40 principals per policy), 100 Resource Groups, 10,000 Projects, and a 64KB per-secret size limit. Large or highly segmented environments should validate these ceilings early.
- **RDP recordings need a conversion step**: Raw RDP session logs are stored in a binary `.asa` format and are not directly reviewable; a separate transcoder step produces a watchable `.mkv` file. This is an extra operational step, not push-button playback.
- **Group membership requests are not native to OPA**: Approval-driven requests for privileged group membership run through Okta Identity Governance (Access Requests), not OPA itself. For customers without OIG, this may introduce a new product dependency rather than an optional add-on.
- **Windows Credential Provider conflict**: Okta's Credential Provider for Windows is explicitly unsupported alongside OPA — flag this for any customer with an existing Windows credential-provider deployment.

Frame gaps as discovery items: "Validate whether [capability] meets the customer's specific requirements, or if OIG integration/additional tooling is needed."

---

## Diagram Component Mapping

When creating Mermaid diagrams for Okta Privileged Access, use these class assignments:

| Okta Component | Mermaid Class |
|---------------|---------------|
| User/client connection request, scheduled cert renewal | `trigger` |
| Active Directory, network devices, external targets | `extSystem` |
| Server Agent, Gateway, Project CA, Secrets Vault | `platform` |
| Okta Workflows automation invoked around OPA events | `workflow` |
| Security Policy evaluation, checkout/elevation approval | `decision` |
| Sudo Command Bundles, Access Requests conditions, Resource Group ownership | `governance` |
| Certificate issuance, credential checkout, sudo grant | `action` |
| Session established, access granted, checkout complete | `endpoint` |
| Access denied, checkout blocked, certificate revoked/expired | `danger` |
| Session recording, signed logs, Okta System Log entries | `audit` |
| Approval request, forced check-in notification | `notify` |
