# URL Verification

The discipline of verifying every external URL before it appears in a delivered document. Required step in Phase 5.5 of the skill workflow.

## The rule

Every URL in a delivered document must be verified in the same session via `web_search` or `web_fetch`. URLs generated from memory are not acceptable, even when the domain is familiar and the path looks reasonable.

## Why this exists

AI models routinely fabricate plausible-looking URLs. The URL has the right domain and a path that follows the apparent site convention, but the actual filename does not exist on the server. This failure mode is especially common with:

- `help.okta.com` — uses internal CMS filenames that often do not match page titles
- AWS documentation — pages have moved across reorganizations
- Microsoft Learn — frequent URL restructuring
- Any vendor documentation that uses content management systems with non-obvious URL schemes

A customer-facing document with broken links is unprofessional and undermines credibility immediately. This rule prevents that.

## Critical anti-pattern: never extrapolate from sibling URLs

**Verifying one URL does NOT verify a related URL**, even when the two pages cover sibling concepts and the URLs look similar in pattern.

Production failure example:
- SAML Identity Provider page: `/security/idp-add-saml.htm` (verified)
- OIDC Identity Provider page: extrapolated to `/security/idp-add-oidc.htm`
- Actual OIDC page: `/integrations/open-id-connect.htm`

The OIDC page is in a different parent directory with a different naming convention. No URL pattern from the SAML page could have predicted it. The extrapolated URL 404'd.

**Every URL must be independently verified**, even if a closely related URL has already been confirmed. Pattern recognition is for understanding failure modes, not for generating new URLs.

## Verification methods

A URL is considered verified when one of the following is true:

1. **`web_fetch` returned a 200 response** with relevant content (not a generic 404 page or marketing redirect)
2. **`web_search` with `site:[domain]` returned the exact URL** in the results, with a snippet confirming the page content matches the intended topic
3. **The URL was provided directly by the user** in the current session (the user is assumed to have tested it)

A URL is NOT verified if:

- It was generated from training knowledge without a search or fetch check in the current session
- A similar URL was verified but this specific path was not
- It was extrapolated from a verified sibling URL
- The root domain resolves but the specific page has not been confirmed
- A previous session verified it (sessions are independent — re-verify)

## Domain risk classifications

| Domain class | Risk | Guidance |
|--------------|------|----------|
| `help.okta.com` | **HIGH** | Never generate from memory. CMS filenames are unpredictable internal identifiers. Always search-then-verify. |
| `docs.aws.amazon.com` | **HIGH** | Pages have moved across multiple AWS doc reorganizations. Always verify. |
| `learn.microsoft.com` | **HIGH** | Frequent URL restructuring; Entra/Azure reorganizations. Always verify. |
| `developer.okta.com` | **LOW** | Predictable patterns (API endpoints, guide slugs). Safe to generate from knowledge but spot-check unfamiliar paths. |
| `docs.aws.amazon.com/[service]/latest/[guide]` | **LOW** for top-level pages | Stable. Verify only when linking to specific sub-pages. |
| `status.[vendor].com`, `trust.[vendor].com` | **NONE** | Simple root domains. No verification needed. |
| Vendor marketing sites (`www.[vendor].com`) | **LOW** | Marketing pages occasionally move. Verify when linking to specific resources or whitepapers. |

When in doubt, verify.

## Known help.okta.com filename patterns

Observed from verified URLs. **Not exhaustive — always verify.** This section exists to help recognize failure modes, not to generate new URLs.

| Page title pattern | Actual filename pattern | Example |
|--------------------|------------------------|---------|
| "[Topic] app integrations" | `apps-about-[topic].htm` | SAML → `apps-about-saml.htm` |
| "Configure [feature]" | varies wildly | Custom domain → `settings-configure-custom-url.htm` |
| "Global Session Policy" | `about-okta-sign-on-policies.htm` | Legacy internal name |
| "Authentication Policies" | `about-authentication-policies.htm` | (Exception — matches the title pattern) |
| "App Sign-In Policies" | `about-app-sign-on-policies.htm` | "sign-on" not "sign-in" in filename |
| Authenticator pages | `/identity-engine/authenticators/...` | NOT under `/security/authenticators/` |
| Enrollment policies | `about-mfa-enrollment-policies.htm` | Under `/policies/` |
| Custom sign-in page | `branding-pages.htm` | Under `/settings/` |
| Authorization servers | `api-config-auth-server.htm` | Not `create-authz-server.htm` |

## Known help.okta.com structural anti-patterns

Higher-level patterns about how Okta organizes CMS paths. Recognizing these prevents entire categories of fabricated URLs.

| AI-generated path | Actual path | Why |
|-------------------|-------------|-----|
| `/security/api-access-management/[page].htm` | `/security/api-config-[page].htm` | No `/api-access-management/` subdirectory exists. Pages are flat under `/security/` with `api-config-` prefix. |
| `/security/authenticators/[page].htm` | `/identity-engine/authenticators/[page].htm` | Authenticator config lives under `/identity-engine/`, not `/security/`. |
| `/security/idp/configure-idp-[protocol].htm` | `/security/idp-add-[protocol].htm` | No `/idp/` subdirectory. SAML uses `idp-add-` prefix. **WARNING: this pattern is SAML-only. OIDC lives at `/integrations/open-id-connect.htm`.** |
| `/identity-governance/entitlements.htm` | `/identity-governance/em/entitlements.htm` | Missing intermediate `/em/` subdirectory. |
| `/apps/apps-overview-[type].htm` | `/apps/apps-about-[type].htm` | Okta uses `about` not `overview` in app topic filenames. |
| `/settings/custom-[feature].htm` | `/settings/settings-configure-custom-[feature].htm` | Settings pages have a `settings-configure-` prefix. |
| `/security/threat-insight.htm` | `/security/threat-insight/ti-index.htm` | Missing intermediate directory with short-code index file. |
| `/end-user/eu-security-settings.htm` | `/identity-engine/enduser/eu-settings.htm` | Wrong parent, wrong subdir name (no hyphen), wrong filename. |
| `/oie/en-us/.../mfa/mfa-reset-factors.htm` | `/en-us/.../mfa/mfa-reset-users.htm` | This page lives in Classic Engine docs (no `/oie/`), and filename is `mfa-reset-users`. |

This table is a living artifact. When new fabrication patterns are discovered, add rows.

## Verification workflow

### During generation (proactive)

When the document needs to cite a vendor doc:
1. Do not write the URL from memory
2. `web_search` with `site:[domain] [topic keywords]`
3. Use the URL returned by search results, not one generated from memory
4. `web_fetch` to confirm the URL resolves and contains relevant content
5. Only then include the URL in the document

### Final pass (defensive)

Before delivery, extract every URL from the document and verify each:

1. Parse the document for all `<a href="">` values, all markdown `[text](url)` links, and any URL appearing in plain text
2. For each URL, classify by domain risk
3. For HIGH-risk domains, every URL must have been verified in the current session — if not, verify now
4. For LOW-risk domains, spot-check unfamiliar paths
5. For NONE-risk domains, no action needed
6. Replace any unverifiable URLs with verified alternatives, or remove the link and note the topic without hyperlinking

### Batch verification for documents with many URLs

For documents with 10+ unique URLs:

1. Extract all unique URLs into a list
2. Group by domain
3. For each HIGH-risk domain, batch-search using `site:[domain] [topic]` queries
4. For any URL that does not appear in search results, the URL is unverified
5. Search for the underlying topic to find the correct URL
6. Replace unverified URLs with verified ones before delivery

This adds time but is essential for documents that will be shared with customers.

## What "verified" does not mean

- The URL working in the past does not mean it works now
- The page existing does not mean it covers what the document claims it covers
- A URL appearing in another document does not transfer verification — re-verify each time

When the page exists but does not cover the claimed topic, that is a different failure (a citation that does not support the claim). Catch this by reading the page content, not just confirming the URL resolves.

## Applying this rule

- HTML artifacts with inline links: verify every `href` value before creating the file
- Markdown documents: verify every `[text](url)` link before delivery
- DOCX documents: verify every hyperlink target before generating
- Quick references / cheat sheets: verify all "📄 Link" references
- Any document generated by this skill: verify all URLs in the Phase 5.5 review step
