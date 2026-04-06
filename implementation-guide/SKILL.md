---
name: implementation-guide
description: Generate professional implementation guide documents with Mermaid flowchart diagrams from use-case requirements. Use this skill whenever a user wants to create an implementation guide, technical whitepaper, use-case document, POC guide, or similar structured technical documentation from a list of use cases or requirements. Also trigger when the user mentions creating diagrams for implementation workflows, generating discovery documents for customer engagements, or converting use-case requirements into professional deliverables. Handles both guided (step-by-step interview) and direct (single-shot) generation modes.
---

# Implementation Guide Generator

Creates professional implementation guide documents from use-case requirements. Produces structured whitepapers with Mermaid flowchart diagrams, feature tables, and discovery items.

## Before Starting

Read these reference files based on what you need:

| File | When to Read |
|------|-------------|
| `references/mermaid-standards.md` | **Always** — before creating any diagram |
| `references/document-template.md` | **Always** — for document structure and formatting |
| `references/okta-oig-reference.md` | When the platform is Okta Identity Governance (OIG) |
| `references/research-protocol.md` | When the platform is NOT Okta, or you need to fill knowledge gaps |
| `references/quality-checklist.md` | Before delivering final output |

## Detect Mode

The skill supports two modes. Detect which one based on context:

### Guided Mode (default for new/uncertain users)
Trigger when:
- User says "help me create" or "walk me through"
- User seems unfamiliar with the output format
- User provides a document without specific instructions

In guided mode, follow the phased interview process (Phase 1-6 below). Ask one question at a time. Confirm before proceeding between phases.

### Direct Mode (for experienced users)
Trigger when:
- User provides a document AND specifies product/customer/format in one message
- User says "just generate it" or "generate the full guide"
- User provides the quick-start prompt template (with all fields filled)

In direct mode, skip the interview. Extract all inputs from the message, generate the full document, then present it for review. Still follow the same document structure and quality standards.

---

## Phase 1: Intake

**Goal:** Get the source document.

If not already provided, ask:

> Please paste or upload your use-case requirements document. It should list use cases with names like "Use Case 1: Employee Onboarding" or similar.

Wait for the document before proceeding.

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

**Goal:** Get product, customer, and section groupings.

Ask these questions (in guided mode, one at a time; in direct mode, extract from context):

1. **Product/platform** — e.g., Okta Identity Governance, SailPoint, Microsoft Entra
2. **Customer name** — for the document title
3. **Section groupings** — suggest logical groupings by functional area, then confirm

When suggesting groupings, organize by common patterns:
- Automated onboarding (joiner)
- Manual/exception onboarding
- Role changes (mover)
- Offboarding (leaver)
- Access requests and approvals
- Access certification/reviews
- Password and credential management
- Compliance and audit
- Reporting

After confirming groupings, if the platform is Okta OIG, read `references/okta-oig-reference.md`. For other platforms, read `references/research-protocol.md` and search for platform-specific capabilities before generating sections.

## Phase 4: Generate

**Goal:** Build each section with diagrams, tables, and discovery items.

Read `references/mermaid-standards.md` and `references/document-template.md` before generating any sections.

### In Guided Mode
Generate ONE section at a time. For each section:
1. Present the section header and use cases covered
2. Write the overview (2-3 paragraphs)
3. Create a Mermaid flowchart diagram (follow mermaid-standards.md exactly)
4. Create a key features table
5. List 3-5 discovery items (assumptions to validate with customer)
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

## Phase 5: Assemble

**Goal:** Add appendices and executive summary.

After all sections are approved (or generated in direct mode):

1. **Appendix A: Use Case to Section Mapping** — table mapping every UC# to its section
2. **Appendix B: Key Components Used** — table of platform components and their purposes
3. **Appendix C: Discovery Items Summary** — consolidated list from all sections
4. **Executive Summary** — written last since it summarizes all content

## Phase 6: Deliver

**Goal:** Produce the final deliverable files.

### Primary Output: Self-Contained HTML

Generate a single HTML file that includes:
- All document content rendered from the markdown
- Mermaid.js loaded from CDN for diagram rendering
- Mermaid code blocks converted to `<div class="mermaid">` elements
- Print-optimized CSS (page breaks before h2, avoid breaks inside diagrams/tables)
- Professional styling matching the template in `references/document-template.md`
- A "Print / Save as PDF" button

**HTML generation steps:**
1. Build the full markdown content
2. Create an HTML document with embedded styles
3. Include Mermaid.js CDN: `https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js`
4. Convert mermaid code blocks to `<div class="mermaid">` tags
5. Ensure HTML entities in mermaid blocks are NOT escaped (`<br>` stays as `<br>`, not `&lt;br&gt;`)
6. Include print CSS from `references/document-template.md`

Save to `/mnt/user-data/outputs/` and present to user.

### Secondary Output: Standalone Renderer

If the user wants to iterate on the markdown separately, also provide:
- The raw markdown source (.md file)
- A copy of the HTML renderer template from `assets/renderer.html`

### Optional: DOCX Output

If the user requests DOCX, generate it using the docx skill. Note that Mermaid diagrams will appear as code blocks in DOCX (not rendered). Direct user to HTML version for diagram viewing.

**If mmdc (mermaid CLI) is available in the environment**, render diagrams to PNG first, then embed in DOCX. Test with: `which mmdc || npx mmdc --version`

### File Naming Convention

```
[customer]-[topic]-implementation-guide.html    # Primary deliverable
[customer]-[topic]-implementation-guide.md      # Markdown source
[customer]-[topic]-implementation-guide.docx    # Optional DOCX
```

---

## Error Recovery

If diagram rendering issues are reported:
1. Check for `<br/>` (should be `<br>`)
2. Check subgraph/end balance
3. Check for single quotes in node text
4. Check for bullet characters (use `-` not `•`)
5. Offer to regenerate the specific diagram
6. If lines are overlapping, simplify using the patterns in `references/mermaid-standards.md`

If user seems stuck or confused:
- Offer to start over, show completed sections, or revise a specific section
- Explain what the current phase is and what comes next

## Key Principles

1. **Use case names must match the source document exactly** — including domain scope
2. **One diagram per section minimum** — every section needs a visual flow
3. **Discovery items are per-section** — don't defer them all to an appendix
4. **Confirm before proceeding** in guided mode — never skip ahead
5. **Quality over speed** — read the quality checklist before delivering
