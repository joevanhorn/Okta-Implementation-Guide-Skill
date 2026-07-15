---
name: implementation-guide
description: Generate professional implementation guide documents with Mermaid flowchart diagrams from use-case requirements. Use this skill whenever a user wants to create an implementation guide, technical whitepaper, use-case document, POC guide, or similar structured technical documentation from a list of use cases or requirements. Also trigger when the user mentions creating diagrams for implementation workflows, generating discovery documents for customer engagements, or converting use-case requirements into professional deliverables. Handles both guided (step-by-step interview) and direct (single-shot) generation modes.
---

# Implementation Guide Generator

Creates professional implementation guide documents from use-case requirements. Produces structured whitepapers with Mermaid flowchart diagrams, feature tables, discovery items, and a fact-verification review pass before delivery.

## Before Starting

Read these reference files based on what you need:

| File | When to Read |
|------|-------------|
| `references/mermaid-standards.md` | **Always** — before creating any diagram |
| `references/document-template.md` | **Always** — for document structure and visual styling |
| `references/url-verification.md` | **Always** — required for any URL that ends up in the output |
| `references/post-generation-review.md` | **Always** — required Phase 5.5 step before delivery |
| `references/quality-checklist.md` | **Always** — final validation before delivery |
| `references/product-portfolio-map.md` | When the product is unspecified, "Okta" is ambiguous, or the opportunity spans multiple products — to map needs → product(s) |
| `references/okta-wic-reference.md` | When the platform is Okta Workforce Identity Cloud (SSO, MFA, FastPass, Universal Directory, LCM) |
| `references/okta-oig-reference.md` | When the platform is Okta Identity Governance (OIG) |
| `references/okta-opa-reference.md` | When the platform is Okta Privileged Access (OPA) |
| `references/okta-itp-reference.md` | When the platform is Okta Identity Threat Protection (ITP) |
| `references/okta-device-access-reference.md` | When the platform is Okta Device Access (Desktop MFA) |
| `references/okta-access-gateway-reference.md` | When the platform is Okta Access Gateway (OAG) |
| `references/auth0-cic-reference.md` | When the platform is Okta Customer Identity Cloud (CIC) / Auth0 |
| `references/auth0-fga-reference.md` | When the platform is Auth0 Fine-Grained Authorization (FGA) |
| `references/research-protocol.md` | When the platform is NOT Okta/Auth0, or when filling knowledge gaps |

The five "Always" files together establish the baseline standard. Platform-specific files (one per product family, e.g. `okta-wic-reference.md`, `auth0-cic-reference.md`) are loaded on demand based on the product. When the product is unclear or the opportunity spans several products, load `product-portfolio-map.md` first to map the customer's needs to the right product(s). More than one product file may be loaded for a multi-product guide.

## Detect Mode

The skill supports two modes. Detect which one based on context:

### Guided Mode (default for new or uncertain users)

Trigger when:
- User says "help me create" or "walk me through"
- User seems unfamiliar with the output format
- User provides a document without specific instructions

In guided mode, follow the phased interview process (Phase 1–6 below). Ask one question at a time. Confirm before proceeding between phases.

### Direct Mode (for experienced users)

Trigger when:
- User provides a document AND specifies product / customer / format in one message
- User says "just generate it" or "generate the full guide"
- User provides a quick-start prompt template with all fields filled

In direct mode, skip the multi-turn interview, but still ask **one consolidated clarifying message** if any of these critical inputs are missing or ambiguous:

- **Customer name** — required for the document title
- **Platform / product** — must be unambiguous. "Okta" alone is not specific: it could mean Workforce Identity Cloud (WIC), Identity Governance (OIG), Privileged Access (OPA), Identity Threat Protection (ITP), Device Access, Access Gateway (OAG), or Customer Identity Cloud (CIC / Auth0). If the product is unclear or the requirements span several of these, load `references/product-portfolio-map.md` and recommend the best-fit product(s) for confirmation.
- **Use cases or topic** — either a use-case document or enough detail to propose use cases
- **Section groupings** — if not obvious from the input

Do not skip clarification entirely just because the user signaled "direct mode."

After clarification, generate the full document, then run the Phase 5.5 review before presenting.

---

## Phase 1: Intake

**Goal:** Get the use cases — from a document or from the user's topic description.

**If the user provides a use-case requirements document:** proceed to Phase 2 with that document.

**If the user provides a topic but no document** (e.g., "Okta SSO for Salesforce" or "Lifecycle Management for Workday"): do NOT insist on a document. Instead, propose a set of use cases based on the topic and ask the user to confirm, add, or remove. Example:

> Based on the topic "[topic]", here are the use cases I'd suggest covering:
>
> 1. UC1: [Proposed use case]
> 2. UC2: [Proposed use case]
> ...
>
> Should I add, remove, or rename any of these?

**If neither a document nor a clear topic is provided**, ask:

> Please paste or upload your use-case requirements document, or describe the topic and platform so I can propose use cases.

Wait for a response before proceeding.

## Phase 2: Analyze

**Goal:** Extract and confirm all use cases.

1. Extract every use case: number, full name, domain/scope if mentioned
2. Present the numbered list back to the user
3. Ask for confirmation — are any missing, misspelled, or wrong scope?

Format:

```
I found [X] use cases:

1. UC1: [Full Name] ([Domain])
2. UC2: [Full Name] ([Domain])
...

Does this look correct?
```

Wait for confirmation. If changes requested, update and re-confirm.

## Phase 3: Configure

**Goal:** Get product, customer, and section groupings — then validate current platform state.

Ask these questions (in guided mode, one at a time; in direct mode, extract from context and consolidate any clarifications into a single message):

1. **Product / platform** — e.g., Okta WIC, Okta Identity Governance, Okta Privileged Access, Customer Identity Cloud (Auth0), SailPoint, Microsoft Entra. If the SE has not named a product, or the requirements clearly span more than one, do **portfolio scoping** first (below) before continuing.
2. **Customer name** — for the document title
3. **Section groupings** — suggest logical groupings by functional area, then confirm

### Portfolio scoping (when the product is unspecified or spans multiple products)

If the product is ambiguous or the customer's needs cross product boundaries, read `references/product-portfolio-map.md`, use its needs → product matrix to **recommend** the best-fit product(s), and **confirm with the SE** before generating. Example:

> Based on these requirements, this looks like **Okta WIC** (SSO + MFA) plus **OIG** (the access reviews you mentioned). Does that match how you're positioning it, or is a different product in scope?

This is a recommendation aid, not a sales script — recommend the honest best fit and flag needs that a different product, a partner, or augmentation (Okta Workflows / custom integration) would serve better. For a multi-product opportunity, load each relevant product reference file and organize sections by product/domain.

When suggesting groupings, organize by common patterns:

- Automated onboarding (joiner)
- Manual / exception onboarding
- Role changes (mover)
- Offboarding (leaver)
- Access requests and approvals
- Access certification / reviews
- Password and credential management
- Compliance and audit
- Reporting

After confirming groupings, load the reference file(s) for the confirmed product(s):

| Confirmed product | Read |
|-------------------|------|
| Okta Workforce Identity Cloud (SSO/MFA/FastPass/UD/LCM) | `references/okta-wic-reference.md` |
| Okta Identity Governance (OIG) | `references/okta-oig-reference.md` |
| Okta Privileged Access (OPA) | `references/okta-opa-reference.md` |
| Okta Identity Threat Protection (ITP) | `references/okta-itp-reference.md` |
| Okta Device Access (Desktop MFA) | `references/okta-device-access-reference.md` |
| Okta Access Gateway (OAG) | `references/okta-access-gateway-reference.md` |
| Okta Customer Identity Cloud (CIC) / Auth0 | `references/auth0-cic-reference.md` |
| Auth0 Fine-Grained Authorization (FGA) | `references/auth0-fga-reference.md` |
| Any other platform (SailPoint, Entra, Ping, etc.) | `references/research-protocol.md`, then search for platform-specific capabilities |

For a multi-product guide, read every relevant file above. Then run the current-state validation below before generating — the reference files are priors, not the source of truth.

### Validate current platform state (required)

**Do not generate content from training data or context alone.** Product offerings, feature names, default behaviors, and UI flows change frequently. Before writing any section:

1. `web_search` for the platform's current product page and documentation home (e.g., `site:okta.com identity governance`, `site:sailpoint.com identity security`)
2. `web_fetch` the official product/feature pages relevant to the confirmed use cases
3. Note any discrepancies between what you know from training data and what the current documentation says — feature renames, deprecated capabilities, new features, changed defaults
4. If a capability referenced in the use cases no longer exists or has been renamed, flag it to the user before generating that section

This step prevents the most damaging class of errors: confidently describing features that have been renamed, deprecated, or restructured since your training cutoff. A guide that references a feature by its old name — or describes a flow that no longer exists — undermines the entire deliverable.

## Phase 4: Generate

**Goal:** Build each section with diagrams, tables, and discovery items.

Read `references/mermaid-standards.md` and `references/document-template.md` before generating any sections.

### In Guided Mode

Generate ONE section at a time. For each section:

1. Present the section header and use cases covered
2. Write the overview (2–3 paragraphs)
3. Create a Mermaid flowchart diagram (follow `mermaid-standards.md` exactly)
4. Create a key features table
5. List 3–5 discovery items (assumptions to validate with customer)
6. Present the complete section
7. Ask: "Does this section look good? I can adjust the diagram, add detail, or change wording."

Only proceed to the next section after confirmation.

### In Direct Mode

Generate all sections, then present the complete document for review. Still follow the same per-section structure.

### Section Format

Follow the template in `references/document-template.md` exactly. Each section must include:

- Use Cases Covered list (exact names from source document)
- Overview paragraphs
- Mermaid flowchart diagram
- Key Features table
- Discovery Items checklist

### URL discipline during generation

If a section needs to cite vendor documentation, follow the workflow in `references/url-verification.md`:

1. Do not write the URL from memory
2. `web_search` with `site:[vendor-domain] [topic]`
3. Use the URL from search results
4. `web_fetch` to confirm content matches

Including unverified URLs at generation time creates more work in Phase 5.5.

## Phase 5: Assemble

**Goal:** Add appendices and executive summary.

After all sections are approved (or generated in direct mode):

1. **Appendix A: Use Case to Section Mapping** — table mapping every UC# to its section
2. **Appendix B: Key Components Used** — table of platform components and their purposes
3. **Appendix C: Discovery Items Summary** — consolidated list from all sections
4. **Executive Summary** — written last, since it summarizes all content

## Phase 5.5: Review

**Goal:** Catch factual errors and broken URLs before delivery. This phase is non-optional for any customer-facing document.

Two sub-passes, in order:

### 5.5.a — URL verification pass

Read `references/url-verification.md`. Extract every URL from the document. Verify each per the rules in that file. Replace any unverifiable URLs.

### 5.5.b — Post-generation fact-checking review

Read `references/post-generation-review.md`. Build a checklist of every verifiable factual claim in the document. Classify each as VERIFIED (cited from a primary source fetched in this session) or TO CHECK (asserted from memory). Verify every TO CHECK item against an authoritative source.

For documents larger than ~3000 lines or with more than ~50 verifiable claims: split the document into sections and run the review as parallel section-level tasks. Maintain a single document-level findings list and "verified despite suspicion" list.

### Surface findings

Before applying any fixes, present findings to the user:

```
Found N factual errors and M items verified-as-correct-despite-suspicion.

ERRORS

#1. [Section / location]
    Currently: [what the doc says]
    Should be: [what the source says]
    Source:    [URL or doc reference]
    Why it's wrong: [one-line explanation]

#2. ...

VERIFIED DESPITE SUSPICION (informational — no fix needed)

- [Claim that looked wrong but is actually correct]
  Why I checked: [what made it look suspicious]
  Why it's right: [authoritative source said so]
```

Wait for acknowledgment. Apply fixes as minimal targeted edits. Re-verify the file is well-formed.

## Phase 6: Deliver

**Goal:** Produce the final deliverable files.

Run `references/quality-checklist.md` as the final validation gate before delivery.

### Primary Output: Self-Contained HTML

Generate a single HTML file using the styled template in `references/document-template.md`. The template uses the dark-navy-gradient header, CSS-counter section numbering, colored callout boxes, and fixed Print/PDF button styling.

**HTML generation steps:**

1. Build the full markdown content
2. Apply the styled HTML template from `references/document-template.md`
3. Include Mermaid.js CDN script
4. Convert mermaid code blocks to `<div class="mermaid">` tags
5. Ensure HTML entities in mermaid blocks are NOT escaped (line breaks stay rendered, not `&lt;br&gt;`)
6. Include the print CSS from the template

Save to `/mnt/user-data/outputs/` and present to user via `present_files`.

### Secondary Output: Standalone Renderer

If the user wants to iterate on the markdown separately, also provide:

- The raw markdown source (`.md` file)
- A copy of the HTML renderer template from `assets/renderer.html`

### Optional: DOCX Output

If the user requests DOCX, generate it using the `docx` skill. Note that Mermaid diagrams will appear as code blocks in DOCX (not rendered). Direct the user to the HTML version for diagram viewing.

If `mmdc` (mermaid CLI) is available in the environment, render diagrams to PNG first, then embed in DOCX. Test with: `which mmdc || npx mmdc --version`

### File Naming Convention

```
[customer]-[topic]-implementation-guide.html    # Primary deliverable
[customer]-[topic]-implementation-guide.md      # Markdown source
[customer]-[topic]-implementation-guide.docx    # Optional DOCX
```

---

## Error Recovery

If diagram rendering issues are reported:

1. Check the line-break convention against the current mermaid version (see `mermaid-standards.md`)
2. Check subgraph / end balance
3. Check for single quotes in node text
4. Check for bullet characters (use `-` not `•`)
5. Offer to regenerate the specific diagram
6. If lines are overlapping, simplify using the patterns in `references/mermaid-standards.md`

If the user seems stuck or confused:

- Offer to start over, show completed sections, or revise a specific section
- Explain what the current phase is and what comes next

## Key Principles

1. **Honest, not impressive.** Capabilities are not overstated. Gaps are documented as discovery items, not papered over. This applies to every platform, not just Okta. Customers can tell when an implementation guide is selling them on something the product cannot actually do — and it permanently damages credibility.

2. **Verified, not pattern-matched.** Specification URIs, version numbers, counts, dates, defaults, UI paths, and URLs are all checked against authoritative sources in the same session. Pattern-matching from training data is the primary source of factual errors in customer-facing documents. Product capabilities, feature names, and UI flows must be validated against current vendor documentation (Phase 3) — never assumed from potentially stale training data.

3. **Use case names match the source document exactly** — including domain scope, capitalization, and spelling.

4. **One diagram per section minimum** — every section needs a visual flow.

5. **Discovery items are per-section** — don't defer them all to an appendix.

6. **Confirm before proceeding** in guided mode — never skip ahead. In direct mode, consolidate clarifications into one message rather than skipping clarification entirely.

7. **Quality over speed.** Phase 5.5 is non-optional. A document with a wrong fact is worse than no document — it damages the customer's trust in everything else.

8. **Right-fit, not one-size.** Map the customer's needs to the best-fit product(s) across the Okta / Auth0 portfolio (see `references/product-portfolio-map.md`), and honestly flag where an adjacent product, a partner, or augmentation (Okta Workflows, custom integration) is the real answer. This is a presales aid, not a sales script — recommending the honest best fit, including "this part isn't a native fit," is what earns the SE credibility. It is the same principle as #1 applied at the product-selection level.
