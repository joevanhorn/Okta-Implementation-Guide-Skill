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

Includes Okta Identity Governance (OIG) domain knowledge out of the box, with a research protocol for other platforms.

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
    ├── document-template.md              # Section structure, HTML template, print CSS
    ├── okta-oig-reference.md             # Okta OIG components, patterns, capabilities
    ├── research-protocol.md              # How to research non-Okta platforms
    └── quality-checklist.md              # Pre-delivery validation checklist
```

Reference files are loaded on-demand — only `SKILL.md` metadata is in context until the skill triggers.

## Requirements

- Claude Pro, Max, Team, or Enterprise plan
- **Code execution and file creation** enabled (Settings → Capabilities)
- **Skills** enabled (Settings → Capabilities)

## Contributing

PRs welcome for:
- Additional platform reference files (SailPoint, Entra, Saviynt, etc.)
- Mermaid diagram patterns for new use case types
- Quality checklist improvements

To add a new platform reference, create `references/[platform]-reference.md` following the structure in `okta-oig-reference.md`, and add a row to the reference file table in `SKILL.md`.

## License

Apache 2.0 — see [LICENSE](LICENSE).
