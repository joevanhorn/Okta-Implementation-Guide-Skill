# Okta Identity Threat Protection (ITP) Reference

## Platform Components

Use these component names consistently across all documents. Map use cases to the appropriate components.

### Core Identity Threat Protection Components

| Component | What It Does | Common Use Cases |
|-----------|-------------|------------------|
| **Identity Threat Protection (ITP) with Okta AI** | Umbrella term for continuous, post-authentication threat detection and response across the identity lifecycle | All continuous threat detection use cases |
| **Risk Engine** | Okta AI-driven engine that continuously evaluates three risk categories — login risk (at authentication), session risk (post-auth, in-session), and entity risk (account compromise likelihood across all sessions/devices) | Real-time risk scoring, anomaly detection |
| **Entity Risk Policy** | Configurable rules (Security > Entity Risk Policy) that map risk level + group membership + detection type to a response action | Automated response to detected compromise |
| **Universal Logout** | Instantly terminates a user's Okta session and revokes tokens/sessions across supported downstream apps | Force logout on compromised session, incident response |
| **Session Revocation** | Ends the Okta session and/or app sessions for a specific detection without necessarily invoking the full Universal Logout app fan-out | Targeted session termination |
| **Shared Signals Framework (SSF)** | OpenID Foundation standard Okta uses to receive signals from and transmit signals to third-party security tools | Bi-directional threat signal exchange |
| **Continuous Access Evaluation Protocol (CAEP)** | SSF profile describing session-state change events (e.g., Session Revoked, Credential Change) | Real-time session risk propagation between vendors |
| **Risk Incident Sharing and Coordination (RISC)** | SSF profile describing account-level change events | Account compromise coordination across vendors |
| **Behavior Detection** | Evaluates deviations from a user's established behavior patterns (velocity, new device, new location) | Anomaly-based risk signals feeding the Risk Engine |
| **Okta ThreatInsight** | Evaluates authentication requests for known-malicious IPs and credential-based attack patterns, before authentication completes | Blocking credential stuffing / brute force at sign-in |
| **Okta Workflows (for ITP)** | Low-code automation invoked as an Entity Risk Policy response action instead of (or in addition to) Universal Logout | Custom remediation: ticket creation, Slack alert, account suspension |

### Supporting Components

| Component | What It Does |
|-----------|-------------|
| **Okta Identity Engine (OIE)** | Required runtime — ITP is not available on Okta Classic Engine |
| **Okta Verify / Okta FastPass** | Phishing-resistant authenticator that also collects device signals feeding session and entity risk evaluation |
| **Device Assurance Policies** | Define device posture requirements (OS version, encryption, screen lock) evaluated continuously, not just at sign-in |
| **Network Zones** | IP/geolocation-based zones continuously evaluated as part of session risk |
| **Adaptive MFA (AMFA)** | Prerequisite capability — step-up authentication policies that ITP's continuous evaluation and entity risk responses build on |
| **System Log** | Where entity risk detections, session violations, and SSF signal events are recorded for audit |
| **Admin Dashboard Risk Widgets** | Surfaces entity risk detections and trends to admins |

### Important Distinctions

**ITP continuous evaluation ≠ standard sign-on/adaptive MFA at login**
- Standard sign-on policies and Adaptive MFA evaluate risk **at the moment of authentication** — once the session is established, those policies are not re-checked unless the user re-authenticates.
- ITP continuously re-evaluates global session and authentication policy conditions, Network Zones, Risk Scoring, Behavior Detection, and Device Assurance **throughout the life of an active session** — a user can be signed in, have their risk profile change mid-session (new IP, device compromise signal, stolen token), and be acted upon without waiting for their next sign-in.
- This is the core value proposition of ITP: threats that emerge *after* a successful, legitimate login are still caught.

**ThreatInsight vs. ITP**
- **ThreatInsight** evaluates authentication requests before they succeed — it is a pre-authentication control that flags/blocks known-malicious IPs and credential-attack patterns.
- **ITP** is the broader, post-authentication continuous protection layer. ThreatInsight is one of several signal sources ITP's Risk Engine consumes (alongside Behavior Detection, device signals, and SSF-received third-party signals).
- Don't conflate them: ThreatInsight = pre-auth gate. ITP = whole-session, whole-identity-lifecycle protection.

**Session risk vs. entity risk**
- **Session risk**: scoped to the current session — did the IP or device context change in a way suggesting token theft or session hijacking?
- **Entity risk**: scoped to the user account across *all* sessions, devices, and apps — including when the user has no active session at all. Entity risk incorporates both Okta-native detections and external signals received over SSF.
- Entity Risk Policy rules act on entity risk, not session risk alone — this is why an SSF signal from an EDR tool (no active Okta session context) can still trigger Universal Logout.

**SSF inbound vs. outbound**
- **Inbound (Okta as receiver)**: third-party tools (CrowdStrike, Microsoft, Zscaler, Palo Alto Networks Cortex XDR, Jamf, Netskope, Cloudflare, and others) push CAEP/RISC events into Okta; the Risk Engine ingests them as entity risk detections.
- **Outbound (Okta as transmitter)**: Okta publishes CAEP events (currently Session Revoked and Credential Change) to registered receivers, letting other systems act on Okta-originated risk signals.
- These are separately configured integrations — supporting one direction does not imply the other is configured.

**ITP vs. Okta Identity Governance (OIG)**
- ITP is a **detection and response** layer for active threats/compromise. OIG is a **governance** layer for who *should* have access and periodic validation of that access.
- They intersect at remediation (an Entity Risk Policy Workflow action can kick off a deprovisioning or access-review process) but ITP does not replace certification campaigns, and OIG certifications do not perform real-time session monitoring.

---

## Common Identity Threat Protection Use Case Patterns

### Detect Compromised Session and Force Re-Auth/Logout

**Typical flow:**
Active session established → Context change detected (new IP, device, impossible travel) mid-session → Risk Engine flags session violation → Entity Risk Policy rule matches → Universal Logout (or Session Revocation) terminates Okta + downstream app sessions → Audit log entry

**Key Okta components:** Risk Engine (session risk), Entity Risk Policy, Universal Logout, Session Revocation, System Log

**Discovery questions:**
- Which downstream apps must be included in Universal Logout, and are they on the supported apps list (native OIN integrations vs. standards-based SAML/OIDC apps with a Global Token Revocation endpoint)?
- Is Okta the primary IdP for all in-scope apps, or are there app sessions Okta cannot see/terminate?
- Should the response be full Universal Logout (all apps) or scoped to specific groups/apps?
- What is acceptable latency between detection and enforced logout?
- Do any apps only support partial logout (e.g., Microsoft 365 revokes refresh tokens but leaves already-issued access tokens valid until expiry) — is that gap acceptable to the customer?

### Risk-Based Step-Up Mid-Session

**Typical flow:**
Session active → Behavior Detection or device signal indicates elevated (not critical) risk → Entity Risk Policy or session policy triggers step-up authentication requirement → User re-authenticates with phishing-resistant factor (Okta Verify/FastPass) → Session risk cleared or session terminated on failure

**Key Okta components:** Risk Engine, Behavior Detection, Device Assurance Policies, Adaptive MFA, Okta Verify/FastPass

**Discovery questions:**
- What risk threshold should trigger step-up vs. full logout vs. no action?
- Which authenticators are acceptable for step-up (phishing-resistant only, or any enrolled factor)?
- Are there apps/flows where step-up is disruptive enough to need a grace period or notification first?
- How should repeated step-up failures be escalated (lock account, notify security team)?

### Ingest EDR/Security-Vendor Threat Signals and Respond

**Typical flow:**
Third-party EDR (CrowdStrike, Microsoft Defender, Zscaler, Palo Alto Cortex XDR, etc.) detects endpoint/network compromise → Signal published via SSF (CAEP/RISC) to Okta as receiver → Risk Engine records entity risk detection → Entity Risk Policy rule matches risk level/detection type → Universal Logout or Workflow remediation executes

**Key Okta components:** Shared Signals Framework (receiver), Risk Engine (entity risk), Entity Risk Policy, Universal Logout, Okta Workflows

**Discovery questions:**
- Which security vendors are in the customer's stack today, and do they have a validated Okta SSF/CAEP integration (native vs. custom-built receiver)?
- What signal types will the vendor actually emit (device compromise, credential change, session revoked), and do they map cleanly to Okta's supported detection types?
- Should every inbound signal trigger the same response, or does severity/detection type need differentiated rules?
- Who owns configuring and testing the receiver endpoint, and is there a fallback if the vendor integration is unavailable (custom SSF receiver build)?
- What is the expected volume of signals, and could false positives from the vendor cause disruptive over-triggering of Universal Logout?

### Share Okta Risk Signals Outbound to Other Tools

**Typical flow:**
Okta detects a risk event (e.g., session revoked, credential changed) → Okta SSF transmitter packages event as a CAEP Security Event Token (SET) → Registered external receiver ingests the signal → Receiving system acts (e.g., SIEM alert, endpoint isolation, third-party session termination)

**Key Okta components:** Shared Signals Framework (transmitter), Risk Engine, System Log

**Discovery questions:**
- Which downstream systems need to consume Okta risk signals, and do they support SSF as a receiver?
- Which CAEP event types are needed (currently Session Revoked and Credential Change) — are those sufficient for the receiving system's use case?
- Is this a one-way notification, or does the customer expect a closed-loop response (receiving system also feeding signals back to Okta)?
- Who monitors for delivery failures to the receiver, and what's the fallback if the receiving system is unreachable?

### Continuous Evaluation of Changing User/Device Risk

**Typical flow:**
User authenticates → Session established → Okta Verify/FastPass and Device Assurance continuously report device posture → Network Zone and behavior continuously reassessed → Any policy condition falls out of compliance → Session violation raised → Entity Risk Policy response executes

**Key Okta components:** Risk Engine, Device Assurance Policies, Network Zones, Behavior Detection, Okta Verify/FastPass, Entity Risk Policy

**Discovery questions:**
- What device posture conditions matter most (encryption, OS patch level, jailbreak/root detection, screen lock)?
- Is Okta Verify/FastPass deployed org-wide, since device signal collection depends on it?
- How should policy handle unmanaged/BYOD devices that can't report the same signal richness as managed devices?
- What is the customer's tolerance for continuous re-evaluation causing mid-session friction vs. security benefit?
- Are there existing AMFA policies in place today that ITP will layer on top of, or does AMFA need to be built first?

---

## Honest Capability Assessment

When creating implementation guides, be accurate about what ITP can and cannot do natively. Do not overstate capabilities.

### ITP Strengths (lean into these)
- Genuine post-authentication, in-session risk evaluation — not just another pre-login adaptive MFA check
- Native, no-extra-infrastructure integration with Okta Verify/FastPass device signals
- Open-standards-based signal exchange (SSF/CAEP/RISC) rather than a proprietary, single-vendor scheme
- Direct Entity Risk Policy configuration in the admin console — no separate console or product needed for basic rules
- Okta Workflows integration gives custom remediation logic without waiting on a product roadmap
- Growing partner ecosystem (CrowdStrike, Microsoft, Zscaler, Palo Alto Networks, Jamf, Netskope, Cloudflare, and others) for bi-directional signal sharing

### Gaps to Acknowledge (document as discovery items, not limitations)
- **Universal Logout app coverage is not universal**: only apps that are Okta-native, in the supported OIN list, or that implement a Global Token Revocation endpoint can be fully logged out. Some supported apps (e.g., Microsoft 365) only perform partial logout — refresh tokens are revoked but already-issued access tokens remain valid until they expire.
- **Scope is limited to Okta-mediated sessions and integrated signal sources**: ITP can only act on what it can see. An app session established outside Okta's control, or an EDR tool without a configured SSF integration, is invisible to the Risk Engine.
- **Dependency on prerequisite capabilities**: ITP requires Okta Identity Engine (not Classic Engine), Universal Directory, SSO, and Adaptive MFA already in place. Organizations early in their Okta maturity (still on Classic Engine, no AMFA) have setup work before ITP delivers value.
- **Dependency on integrated signal sources**: the value of inbound SSF signal ingestion is only as good as the customer's actual security stack and whether their specific vendor/product tier has a validated Okta SSF integration versus requiring a custom-built receiver.
- **Not a governance/access-review substitute**: ITP responds to active threats; it does not replace periodic access certification, entitlement review, or SoD enforcement (that's OIG's job).
- **Licensing is a separate SKU**: ITP with Okta AI is licensed independently of base Workforce Identity Cloud — confirm current entitlement/licensing status with the account team rather than assuming it's included.

Frame gaps as discovery items: "Validate whether [capability] meets the customer's specific requirements, or if augmentation via Workflows/custom SSF receiver is needed."

---

## Diagram Component Mapping

When creating Mermaid diagrams for Okta ITP, use these class assignments:

| Okta Component | Mermaid Class |
|---------------|---------------|
| EDR/security vendor signal, external trigger event | `trigger` or `extSystem` |
| CrowdStrike, Microsoft, Zscaler, Palo Alto Networks, other SSF partners | `extSystem` |
| Risk Engine, Identity Engine, continuous session evaluation | `platform` |
| Okta Workflows (remediation automation) | `workflow` |
| Session violation check, risk level evaluation, policy match | `decision` |
| Entity Risk Policy, Device Assurance Policy, Network Zone evaluation | `governance` |
| Universal Logout execution, session revocation, step-up enforcement | `action` |
| Session cleared, account confirmed safe | `endpoint` |
| Access denied, session terminated, account suspended | `danger` |
| System Log entry, entity risk detection record | `audit` |
| Security team alert, Slack/email notification | `notify` |
