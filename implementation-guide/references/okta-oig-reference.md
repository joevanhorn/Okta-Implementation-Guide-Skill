# Okta Identity Governance (OIG) Reference

## Platform Components

Use these component names consistently across all documents. Map use cases to the appropriate components.

### Core Identity Governance Components

| Component | What It Does | Common Use Cases |
|-----------|-------------|------------------|
| **Okta Identity Governance (OIG)** | Umbrella term for governance capabilities within Okta | All governance use cases |
| **Access Certifications** | Periodic review campaigns where managers/app owners validate user access | Access reviews, recertification, compliance audits |
| **Access Requests (RCAR)** | Self-service access request portal with approval workflows | Role-based access requests, elevated access, JIT access |
| **Request Types** | Configurable request forms with conditional field logic (show/hide fields) | Delegated admin flows, custom intake forms |
| **Entitlement Management** | Discover, catalog, and govern granular permissions from downstream apps | Fine-grained access reviews, SoD enforcement |
| **Governance Reports** | Compliance and audit reporting across identity lifecycle | Audit evidence, regulatory compliance |
| **Okta Workflows** | Low-code automation platform for identity event-driven processes | Custom provisioning logic, notifications, data transformation |
| **Lifecycle Management (LCM)** | Automated joiner/mover/leaver provisioning based on HR events | Onboarding, role changes, offboarding |
| **Group Rules** | Dynamic group membership based on user attributes | Automatic app/resource assignment by department, role, location |
| **Okta Expression Language (OEL)** | Attribute transformation language for profile mappings | Username generation, attribute derivation |

### Supporting Components

| Component | What It Does |
|-----------|-------------|
| **Universal Directory (UD)** | Centralized user/group store with custom attributes |
| **Profile Mastering** | Controls which source (HR, AD, manual) is authoritative for each attribute |
| **Inline Hooks** | Real-time callouts during authentication/registration for custom logic |
| **Event Hooks** | Async notifications to external systems when Okta events occur |
| **Okta Integration Network (OIN)** | Pre-built app integrations catalog |
| **SCIM Provisioning** | Automated user/group sync to downstream applications |
| **Linked Objects** | Define relationships between users (manager, delegate, sponsor) |

### Important Distinctions

**Request Types ≠ RCAR (Access Requests)**
- **Request Types**: Configurable forms with conditional field logic. Used for custom intake processes like delegated admin, service requests, or any structured workflow that needs dynamic form fields.
- **RCAR (Access Requests)**: Self-service catalog for requesting access to applications and resources with built-in approval workflows, time-bound access, and conditions.
- They serve different purposes. Don't conflate them.

**OEL Limitations**
- OEL is NOT suitable for constructing nested JSON structures
- OEL is for attribute transformation (string manipulation, conditionals, defaults)
- For complex data transformation, use Okta Workflows instead

---

## Common IGA Use Case Patterns

### Joiner (Onboarding)

**Typical flow:**
HR event → Identity creation in UD → Profile mastering → Group rule evaluation → App assignment → SCIM provisioning → Notification

**Key Okta components:** LCM, Universal Directory, Group Rules, SCIM Provisioning, Okta Workflows (for custom logic)

**Discovery questions:**
- What is the authoritative HR source? (Workday, SuccessFactors, BambooHR, etc.)
- What attributes drive group membership and app assignment?
- Are there different onboarding flows by employee type (salaried, hourly, contractor)?
- What is the timing expectation? (Day-of, pre-hire provisioning?)
- What downstream apps need provisioning vs SSO-only?

### Mover (Role Change)

**Typical flow:**
HR attribute change → Profile update → Group rule re-evaluation → Access adjustment → Certification trigger (optional) → Notification

**Key Okta components:** LCM, Group Rules, Access Certifications, Okta Workflows

**Discovery questions:**
- What attributes change during a role change? (department, title, manager, cost center)
- Should old access be removed immediately or reviewed via certification?
- Are there time-bound transition periods where both old and new access coexist?
- Who is notified of role changes?

### Leaver (Offboarding)

**Typical flow:**
HR termination event → Account suspension → App deprovisioning → License reclamation → Audit log → Delayed account deletion

**Key Okta components:** LCM, SCIM Provisioning, Okta Workflows, Governance Reports

**Discovery questions:**
- What is the SLA from HR termination to access removal?
- Is there a suspension period before full deprovisioning?
- Which apps need immediate deprovisioning vs graceful removal?
- What data retention/transfer requirements exist?
- Are there compliance requirements for audit trail of offboarding?

### Access Requests and Approvals

**Typical flow:**
User requests access → Policy evaluation → Manager approval → (Optional: resource owner approval) → Access granted → Time-bound if applicable → Certification scheduled

**Key Okta components:** RCAR, Okta Workflows (for custom approval routing), Access Certifications

**Discovery questions:**
- What is the approval chain? (Single manager, multi-level, resource owner?)
- Are there any auto-approval policies for low-risk requests?
- Should access be time-bound by default?
- What self-service catalog items are needed?

### Access Certification

**Typical flow:**
Campaign scheduled → Reviewer notified → Access reviewed per user/app → Approve/revoke decisions → Remediation executed → Report generated

**Key Okta components:** Access Certifications, Governance Reports, Okta Workflows (for remediation)

**Discovery questions:**
- What is the certification frequency? (Quarterly, semi-annual, annual)
- Who are the reviewers? (Managers, app owners, both?)
- What happens to unreviewed items at campaign close? (Auto-revoke, escalate, extend?)
- Are there different campaign types for different risk levels?
- What downstream remediation is needed when access is revoked?

### Separation of Duties (SoD)

**Typical flow:**
SoD policy defined → Access request triggers policy check → Violation detected → Escalation/exception workflow → Decision recorded → Audit trail

**Key Okta components:** Entitlement Management, RCAR (conditions), Okta Workflows, Access Certifications

**Discovery questions:**
- What SoD rules need enforcement? (Specific conflicting entitlements)
- Are SoD checks preventive (block at request time) or detective (flag in certification)?
- What is the exception process for legitimate SoD violations?
- At what granularity? (App-level, entitlement-level, role-level?)

---

## Honest Capability Assessment

When creating implementation guides, be accurate about what OIG can and cannot do natively. Do not overstate capabilities.

### OIG Strengths (lean into these)
- Tight integration between governance and the identity platform (single pane of glass)
- Lifecycle automation with direct provisioning (no separate connector infrastructure)
- Okta Workflows for flexible custom logic without code deployment
- Pre-built OIN integrations for rapid app onboarding
- Access Requests with built-in approval workflows and time-bound access
- Real-time policy enforcement at the point of access

### OIG Gaps to Acknowledge (document as discovery items, not limitations)
- **Identity correlation across sources**: Complex multi-source identity matching may need Workflows customization
- **Cross-application SoD**: Entitlement-level SoD across apps is maturing; may need Workflows augmentation
- **Native risk scoring**: ITP provides threat signals but risk-based governance scoring is not deeply integrated with certification campaigns yet
- **Reporting depth**: Governance Reports covers core scenarios; complex custom reporting may need data export to external BI tools
- **Role mining**: OIG does not include automated role mining/discovery; role definitions are manual or imported

Frame gaps as discovery items: "Validate whether [capability] meets the customer's specific requirements, or if augmentation via Workflows/integration is needed."

---

## Diagram Component Mapping

When creating Mermaid diagrams for Okta OIG, use these class assignments:

| Okta Component | Mermaid Class |
|---------------|---------------|
| HR system, AD, external triggers | `trigger` or `extSystem` |
| Universal Directory, LCM, Identity Engine | `platform` |
| Okta Workflows | `workflow` |
| Policy checks, approval decisions | `decision` |
| Group Rules, Access Certifications, SoD | `governance` |
| App assignment, SCIM provisioning | `action` |
| Process complete, account active | `endpoint` |
| Access denied, account disabled | `danger` |
| Audit log, compliance report | `audit` |
| Email/Slack notifications | `notify` |
