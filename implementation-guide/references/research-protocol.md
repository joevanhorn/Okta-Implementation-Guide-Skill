# Research Protocol

Use this when generating implementation guides for platforms where you lack deep product knowledge, or when you need to fill gaps for any platform.

## When to Research

- The user names a platform you don't have detailed component knowledge for
- You're unsure whether a specific capability exists on the platform
- The use case involves a niche feature or recent product addition
- You need accurate component/feature names (not guesses)

## Research Approach

### Step 1: Search official documentation first

Search for `[platform] [capability] documentation site:help.[vendor].com OR site:docs.[vendor].com`

Examples:
- `SailPoint access certification documentation site:documentation.sailpoint.com`
- `Microsoft Entra access reviews site:learn.microsoft.com`
- `Saviynt separation of duties site:docs.saviynt.com`

### Step 2: Search for real-world implementations

If official docs don't give enough context for a practical guide:
- `[platform] [use case] implementation best practices`
- `[platform] [use case] customer experience site:reddit.com`
- `[platform] [use case] review site:peerspot.com OR site:g2.com`

### Step 3: Search for known limitations

Before stating a platform can do something, verify:
- `[platform] [capability] limitations OR issues OR problems`
- `[platform] [capability] workaround`

This prevents overstating capabilities in the implementation guide.

## How to Handle Uncertainty

If you cannot verify a capability:
1. Do NOT guess or hallucinate feature names
2. Add a discovery item: "Validate that [platform] supports [capability] natively, or identify required customization"
3. Use generic descriptions: "The platform processes the request" rather than naming a specific component you're unsure about
4. Tell the user: "I'm not confident about [platform's] specific approach to [capability]. I'd recommend verifying this section with a platform SME."

## Common IGA Platforms and Documentation Roots

| Platform | Documentation URL Pattern |
|----------|--------------------------|
| Okta OIG | help.okta.com, developer.okta.com |
| SailPoint IdentityNow | documentation.sailpoint.com |
| SailPoint IIQ | community.sailpoint.com |
| Saviynt | docs.saviynt.com |
| Microsoft Entra ID Governance | learn.microsoft.com/entra |
| CyberArk Identity | docs.cyberark.com |
| Omada Identity | docs.omadaidentity.com |
| One Identity | support.oneidentity.com |
| ForgeRock/Ping Identity | docs.pingidentity.com |
| MidPoint (Evolveum) | docs.evolveum.com |

## Mapping Generic Concepts to Platform Terms

Different platforms use different names for the same concepts. When researching, search for BOTH the generic term and common platform-specific terms:

| Generic Concept | Common Platform Terms |
|----------------|----------------------|
| Access certification | Access review, recertification, attestation, entitlement review |
| Access request | Shopping cart, self-service request, access catalog, request portal |
| Lifecycle management | Joiner-mover-leaver, JML, identity lifecycle, provisioning |
| Separation of duties | SoD, incompatible access, toxic combinations, policy violations |
| Role management | Role mining, role engineering, RBAC, business roles |
| Entitlement management | Fine-grained access, permissions catalog, entitlement governance |
| Workflow/automation | Orchestration, process automation, business logic |
| Provisioning | Account management, fulfillment, target system management |
