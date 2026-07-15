# Implementation Guide Generator

A Claude skill that generates professional implementation guide documents with Mermaid flowchart diagrams from use-case requirements.

Built for solutions engineers and architects who need to quickly produce customer-facing implementation guides from use-case documents.

## What It Does

Give it a use-case requirements document, and it produces a polished implementation guide with:

- Sections grouped by functional area (onboarding, offboarding, access requests, etc.)
- Mermaid flowchart diagrams for each section
- Key features tables
- Discovery items (assumptions to validate with the customer)
- Executive summary and appendices
- Print-ready HTML output with rendered diagrams

Supports both a **guided mode** (step-by-step interview) and a **direct mode** (dump your doc and get the output).

Includes deep domain knowledge for the full Okta and Auth0 portfolio out of the box — Workforce Identity Cloud (WIC), Identity Governance (OIG), Privileged Access (OPA), Identity Threat Protection (ITP), Device Access, Access Gateway (OAG), Customer Identity Cloud (CIC / Auth0), and Auth0 Fine-Grained Authorization (FGA) — plus a solution-mapping guide that helps you pick the right product(s) for an opportunity, and a research protocol for non-Okta platforms.

## What's New (July 2026)

**Full Okta + Auth0 portfolio coverage.** The skill now ships product-knowledge reference files for the whole portfolio — Workforce Identity Cloud, Identity Governance, Privileged Access, Identity Threat Protection, Device Access, Access Gateway, Customer Identity Cloud (Auth0), and Auth0 Fine-Grained Authorization — not just OIG. Each follows the same honest, gaps-as-discovery-items structure.

**Solution mapping for presales.** A new `product-portfolio-map.md` reference lets the skill map a customer's *needs* to the right product(s) — so you don't have to name the product up front — and supports multi-product guides. Phase 3 gained a portfolio-scoping step that recommends the best-fit product(s) for your confirmation. Framing stays honest: it recommends the right fit and flags where an adjacent product or augmentation is the real answer.

## What's New (May 2026)

**Phase 5.5 — Fact-checking review pass.** Every document now goes through a mandatory two-pass review before delivery: URL verification (5.5.a) and post-generation fact-checking (5.5.b). The bot inventories every verifiable claim, checks it against authoritative sources, and presents findings for your approval before applying fixes.

**Current-state validation.** The skill now `web_search` + `web_fetch`es vendor documentation before generating content — it won't operate on potentially stale training data. Feature renames, deprecated capabilities, and changed defaults are flagged before they end up in your deliverable.

**URL verification discipline.** New reference file with domain risk classifications, known `help.okta.com` anti-patterns, and the critical rule: never extrapolate URLs from sibling pages. Every URL in the output is verified in-session.

**Styled HTML template.** The output now uses a dark-navy-gradient header, CSS-counter section numbering, four callout variants (info/warn/tip/danger), navigation breadcrumbs, and refined print CSS. This replaces the previous minimal template.

**Topic-only intake.** You no longer need a use-case requirements document to get started. Describe a topic ("Okta SSO for Salesforce") and the skill proposes use cases for your confirmation.

**Direct mode tightened.** Direct mode now asks one consolidated clarifying question when critical inputs are missing (customer name, platform, use cases, section groupings) instead of silently assuming.

**47-test validation suite.** Structural tests, mermaid validator tests, URL pattern tests, review fixture tests, and HTML template tests — all stdlib-only Python, runnable with `python3 tests/run_tests.py`.

### Updating

If you installed via symlink + git clone, just `git pull`. If you copied the files, re-copy the `implementation-guide/` directory and add the new `tests/` directory.

## Installation

### Claude.ai / Claude Desktop

1. Download the latest `implementation-guide.skill` from [Releases](../../releases)
2. In Claude, go to **Settings → Customize → Skills**
3. Click **"+" → "+ Create skill"**
4. Upload the `.skill` file
5. Toggle the skill **on**

> The `.skill` file is a ZIP archive. If your Claude version requires a `.zip`, rename the extension.

### Claude Code

Clone this repo and symlink (or copy) the skill folder into your skills directory:

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/implementation-guide-skill.git

# Option A: Symlink for auto-updates on git pull
ln -s "$(pwd)/implementation-guide-skill/implementation-guide" ~/.claude/skills/implementation-guide

# Option B: Copy
cp -r implementation-guide-skill/implementation-guide ~/.claude/skills/
```

For project-scoped installation:

```bash
cp -r implementation-guide-skill/implementation-guide your-project/.claude/skills/
```

### Cowork

Same as Claude Code — copy or symlink the `implementation-guide/` folder into `~/.claude/skills/`.

## Usage

### Guided Mode

Start a conversation and say something like:

> "Help me create an implementation guide from this use-case document."

Then paste or upload your document. The skill will walk you through extracting use cases, confirming groupings, and reviewing each section before assembly.

### Direct Mode

Provide everything in one message:

> "Generate a full implementation guide from this document. Platform: Okta OIG. Customer: Acme Corp."
>
> [paste document]

The skill will generate the complete guide and present it for review.

### What You Get

The primary output is a self-contained HTML file with:
- Rendered Mermaid diagrams (via CDN)
- Print-optimized CSS (use browser Print → Save as PDF)
- Professional styling

The skill can also provide raw Markdown and the standalone renderer template for iterative editing.

## Skill Structure

```
implementation-guide/
├── SKILL.md                              # Core instructions (loaded on trigger)
├── assets/
│   └── renderer.html                     # Standalone Markdown+Mermaid renderer
└── references/
    ├── mermaid-standards.md              # Diagram syntax, colors, overlap prevention
    ├── document-template.md              # Section structure, styled HTML template, print CSS
    ├── url-verification.md               # URL verification discipline and anti-patterns
    ├── post-generation-review.md         # Phase 5.5 fact-checking procedure
    ├── quality-checklist.md              # Pre-delivery validation checklist + mermaid validator
    ├── product-portfolio-map.md          # Solution mapping: needs -> product(s), multi-product guidance
    ├── okta-wic-reference.md             # Okta Workforce Identity Cloud (SSO, MFA, FastPass, UD, LCM)
    ├── okta-oig-reference.md             # Okta Identity Governance components, patterns, capabilities
    ├── okta-opa-reference.md             # Okta Privileged Access (SSH/RDP, checkout, sudo bundles)
    ├── okta-itp-reference.md             # Okta Identity Threat Protection (continuous risk, SSF)
    ├── okta-device-access-reference.md   # Okta Device Access (Desktop MFA, OS login)
    ├── okta-access-gateway-reference.md  # Okta Access Gateway (legacy on-prem app SSO)
    ├── auth0-cic-reference.md            # Customer Identity Cloud / Auth0 (CIAM)
    ├── auth0-fga-reference.md            # Auth0 Fine-Grained Authorization (ReBAC / OpenFGA)
    └── research-protocol.md              # How to research non-Okta/Auth0 platforms
tests/
├── run_tests.py                          # Test orchestrator (47 tests, stdlib only)
├── test_skill_structure.py               # Required files, phases, principles
├── test_mermaid_validator.py             # Mermaid syntax validation rules
├── test_url_patterns.py                  # URL verification reference content
├── test_review_fixtures.py              # Fact-checking categories and procedure
├── test_html_template.py                 # Styled template structural elements
└── fixtures/                             # Test fixtures (buggy doc, mermaid samples)
```

The five "Always" reference files (`mermaid-standards`, `document-template`, `url-verification`, `post-generation-review`, `quality-checklist`) are loaded every time. Platform-specific files (`okta-oig-reference`, `research-protocol`) are loaded on demand.

## Requirements

- Claude Pro, Max, Team, or Enterprise plan
- **Code execution and file creation** enabled (Settings → Capabilities)
- **Skills** enabled (Settings → Capabilities)

## Contributing

The full Okta and Auth0 portfolio ships in the box. PRs welcome for:
- Additional **non-Okta** platform reference files (SailPoint, Entra, Saviynt, Ping, etc.)
- Deeper use-case patterns for the existing Okta/Auth0 product files
- Mermaid diagram patterns for new use case types
- Quality checklist improvements

To add a new platform reference, create `references/[platform]-reference.md` following the structure in `okta-oig-reference.md`, and add a row to the reference file table in `SKILL.md`.

## License

Apache 2.0 — see [LICENSE](LICENSE).
