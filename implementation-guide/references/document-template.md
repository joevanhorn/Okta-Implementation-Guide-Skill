# Document Template

## Overall Structure

```markdown
# [Product]: [Customer] Use Case Implementation Guide

## Executive Summary
[3–5 sentence overview, total use case count, key functional areas covered]

## Section 1: [Functional Area Name]
[section content — see Section Template below]

## Section 2: [Functional Area Name]
[section content]

...

## Appendix A: Use Case to Section Mapping
[table]

## Appendix B: Key Components Used
[table]

## Appendix C: Discovery Items Summary
[consolidated list]
```

---

## Section Template

Each section follows this exact structure:

```markdown
## Section [N]: [Functional Area Name]

**Use Cases Covered:**
- UC[#]: [Full Use Case Name] ([Domain/Scope])
- UC[#]: [Full Use Case Name] ([Domain/Scope])

### Overview

[2–3 paragraphs explaining:
 - What business problem this section addresses
 - How the platform handles it at a high level
 - What makes this approach better than manual processes]

### How It Works

```mermaid
flowchart TD
    [diagram following mermaid-standards.md]
```

[1–2 paragraphs explaining the flow shown in the diagram.
 Walk through the key steps and decision points.]

### Key Features

| Feature | Purpose |
|---------|---------|
| [Feature name] | [What it does and why it matters] |
| [Feature name] | [What it does and why it matters] |
| [Feature name] | [What it does and why it matters] |

### Discovery Items

- [ ] [Question or assumption to validate with customer]
- [ ] [Question or assumption to validate with customer]
- [ ] [Question or assumption to validate with customer]
```

---

## Use Case Naming Rules

- Names MUST match the source document exactly — including capitalization and domain scope
- Always include domain scope in parentheses when present: `(NNS Corp Domain)`, `(All Domains)`
- Format in lists: `- UC#: Full Use Case Name (Domain)`
- Never abbreviate or rephrase use case names

---

## Appendix Formats

### Appendix A: Use Case to Section Mapping

| Use Case | Name | Section |
|----------|------|---------|
| UC1 | [Full Name] ([Domain]) | Section 1: [Area] |
| UC2 | [Full Name] ([Domain]) | Section 1: [Area] |
| UC3 | [Full Name] ([Domain]) | Section 2: [Area] |

### Appendix B: Key Components Used

| Component | Purpose | Sections Used |
|-----------|---------|---------------|
| [Component] | [What it does] | 1, 3, 5 |
| [Component] | [What it does] | 2, 4 |

### Appendix C: Discovery Items Summary

Consolidated from all sections, grouped by section:

**Section 1: [Name]**
- [ ] [Discovery item]
- [ ] [Discovery item]

**Section 2: [Name]**
- [ ] [Discovery item]

---

## Discovery Item Guidelines

Good discovery items are:

- **Specific** — "What HRIS fields map to the display name attribute?" not "How does HRIS work?"
- **Actionable** — something the customer can answer or demonstrate
- **Assumption-revealing** — makes hidden assumptions explicit
- **Scoped** — tied to a specific use case or section

Common categories:

- Source system integrations (what fields, what format, what frequency)
- Approval chain structure (who approves, how many levels, escalation)
- Exception handling (what happens when the happy path fails)
- Timing requirements (SLAs, batch windows, real-time needs)
- Existing processes being replaced (current manual steps)
- Compliance requirements (audit retention, regulatory constraints)

---

## HTML Output Template

The output HTML uses a styled template with:

- Dark navy gradient header bar
- CSS-counter section numbering (h2 elements auto-numbered with a colored prefix)
- Colored callout boxes for info, warn, tip, danger
- Fixed Print / PDF button in the bottom-right
- Print-optimized CSS that handles page breaks correctly

Full template (use this exactly):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Product]: [Customer] Implementation Guide</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        @page { size: letter; margin: 0.5in 0.6in; }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #1a1f2e;
            max-width: 960px;
            margin: 0 auto;
            padding: 20px;
            background: #fff;
            counter-reset: section;
        }

        /* Document header */
        .doc-header {
            background: linear-gradient(135deg, #1a1f2e 0%, #2d3548 100%);
            color: white;
            padding: 30px 35px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        .doc-header h1 { font-size: 22pt; margin-bottom: 6px; border: none; padding: 0; color: white; }
        .doc-header .subtitle { opacity: 0.85; font-size: 11pt; }
        .doc-header .meta {
            margin-top: 15px;
            display: flex;
            gap: 25px;
            font-size: 9pt;
            opacity: 0.7;
            flex-wrap: wrap;
        }

        /* Section headings with CSS counters */
        h2 {
            color: #1a1f2e;
            font-size: 15pt;
            margin: 35px 0 15px 0;
            padding-bottom: 6px;
            border-bottom: 2px solid #007dc1;
            counter-increment: section;
        }
        h2::before {
            content: counter(section) ". ";
            color: #007dc1;
        }
        /* Don't number appendices automatically — use explicit "Appendix A" text */
        h2.no-counter { counter-increment: none; }
        h2.no-counter::before { content: ""; }

        h3 { color: #333; font-size: 12pt; margin: 20px 0 10px 0; }
        h4 { color: #333; font-size: 11pt; margin: 16px 0 8px 0; }

        p { margin: 8px 0; }

        /* Callout boxes */
        .callout {
            border-radius: 6px;
            padding: 14px 16px;
            margin: 15px 0;
            font-size: 10pt;
            display: flex;
            gap: 12px;
            align-items: flex-start;
        }
        .callout-icon { font-size: 16pt; line-height: 1; flex-shrink: 0; }
        .callout-body { flex: 1; }
        .callout-body strong { display: block; margin-bottom: 3px; }

        .callout-info   { background: #e3f2fd; border: 1px solid #90caf9; color: #0d47a1; }
        .callout-warn   { background: #fff3cd; border: 1px solid #ffc107; color: #856404; }
        .callout-tip    { background: #e8f5e9; border: 1px solid #a5d6a7; color: #1b5e20; }
        .callout-danger { background: #ffebee; border: 1px solid #ef9a9a; color: #b71c1c; }

        /* Navigation breadcrumb (UI paths) */
        .nav-path {
            background: #f5f5f5;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            padding: 6px 12px;
            font-size: 9.5pt;
            font-family: 'Monaco', 'Menlo', monospace;
            display: inline-block;
            margin: 4px 0;
        }
        .nav-path .sep { color: #999; margin: 0 4px; }

        /* Code blocks */
        pre {
            background: #1e1e2e;
            color: #cdd6f4;
            padding: 16px 20px;
            border-radius: 6px;
            overflow-x: auto;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 9.5pt;
            line-height: 1.5;
            margin: 12px 0;
        }
        pre code { background: none; padding: 0; color: inherit; }
        code {
            background: #f0f0f0;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
            font-size: 9.5pt;
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 12px 0;
            font-size: 10pt;
        }
        th, td { border: 1px solid #ddd; padding: 8px 12px; text-align: left; vertical-align: top; }
        th { background: #1a1f2e; color: white; font-weight: 600; }
        tr:nth-child(even) { background: #fafafa; }

        /* Numbered step lists */
        .steps { counter-reset: step; list-style: none; padding: 0; }
        .steps li {
            counter-increment: step;
            margin: 10px 0;
            padding-left: 36px;
            position: relative;
        }
        .steps li::before {
            content: counter(step);
            position: absolute;
            left: 0;
            top: 1px;
            background: #007dc1;
            color: white;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10pt;
            font-weight: 600;
        }

        /* Mermaid diagrams */
        .mermaid {
            background: #fafafa;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
            text-align: center;
        }

        /* Discovery items panel */
        .discovery {
            background: #fff8e1;
            border: 1px solid #ffe082;
            border-radius: 6px;
            padding: 14px 16px;
            margin: 15px 0;
        }
        .discovery h4 { color: #f57f17; margin-bottom: 8px; font-size: 10pt; }
        .discovery ul { padding-left: 20px; font-size: 10pt; }
        .discovery li { margin: 4px 0; }

        /* Print button */
        .print-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #007dc1;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 11pt;
            font-weight: 500;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            z-index: 100;
        }
        .print-btn:hover { background: #0066a1; }

        /* Print styles */
        @media print {
            .print-btn { display: none !important; }
            body { padding: 0; font-size: 10pt; }
            .doc-header { break-after: avoid; }
            h2 { break-before: page; }
            h2:first-of-type, .doc-header + h2 { break-before: avoid; }
            h1, h2, h3, h4 { break-after: avoid; }
            pre, .mermaid, table, .callout, .discovery { break-inside: avoid; }
            pre { background: #f5f5f5 !important; color: #1a1f2e !important; border: 1px solid #ddd; }
            .mermaid svg { max-width: 100%; max-height: 500px; height: auto; }
            p { orphans: 3; widows: 3; }
        }
    </style>
</head>
<body>

<button class="print-btn" onclick="window.print()">🖨️ Print / PDF</button>

<div class="doc-header">
    <h1>[Document Title]</h1>
    <div class="subtitle">[Product]: [Customer] Implementation Guide</div>
    <div class="meta">
        <span>Customer: [Customer Name]</span>
        <span>Platform: [Platform]</span>
        <span>Date: [YYYY-MM-DD]</span>
    </div>
</div>

<!-- DOCUMENT CONTENT GOES HERE -->
<!-- - Use <h2> for main sections (auto-numbered via CSS counter) -->
<!-- - Use <h2 class="no-counter"> for appendices and unnumbered sections -->
<!-- - Use <div class="callout callout-info"> (or -warn, -tip, -danger) for callouts -->
<!-- - Use <ol class="steps"> for numbered procedures -->
<!-- - Use <span class="nav-path">A<span class="sep">›</span>B</span> for UI paths -->
<!-- - Convert markdown mermaid code blocks to <div class="mermaid"> elements -->
<!-- - Ensure HTML entities in mermaid divs are NOT escaped -->

<script>
    mermaid.initialize({
        startOnLoad: true,
        theme: 'default',
        securityLevel: 'loose',
        flowchart: {
            useMaxWidth: true,
            htmlLabels: true,
            curve: 'basis'
        }
    });
</script>
</body>
</html>
```

### Critical HTML generation notes

- Mermaid code blocks MUST be `<div class="mermaid">`, not `<pre><code>`
- HTML entities inside mermaid divs must NOT be escaped — line breaks render, not `&lt;br&gt;`
- Include `securityLevel: 'loose'` in mermaid init to allow HTML labels
- Include `curve: 'basis'` for smoother line routing
- Appendices use `<h2 class="no-counter">` so they don't get auto-numbered (the "Appendix A:" text in the heading is explicit)

### Callout usage

| Class | Icon | Purpose |
|-------|------|---------|
| `callout-info` | ℹ️ | Neutral context or background information |
| `callout-warn` | ⚠️ | Common pitfall, version compatibility issue, surprising behavior |
| `callout-tip` | 💡 | Helpful pattern, optimization, recommendation |
| `callout-danger` | 🚫 | Action that will break things or cause data loss |

Example:

```html
<div class="callout callout-warn">
    <span class="callout-icon">⚠️</span>
    <div class="callout-body">
        <strong>Version compatibility</strong>
        Clients below version X cannot authenticate via this method. Validate client versions across the fleet before enabling.
    </div>
</div>
```
