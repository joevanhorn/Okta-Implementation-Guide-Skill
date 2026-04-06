# Document Template

## Overall Structure

```markdown
# [Product]: [Customer] Use Case Implementation Guide

## Executive Summary
[3-5 sentence overview, total use case count, key functional areas covered]

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

[2-3 paragraphs explaining:
 - What business problem this section addresses
 - How the platform handles it at a high level
 - What makes this approach better than manual processes]

### How It Works

```mermaid
flowchart TD
    [diagram following mermaid-standards.md]
```

[1-2 paragraphs explaining the flow shown in the diagram.
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

When generating the final HTML file, use this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Product]: [Customer] Implementation Guide</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        /* Base styles */
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            line-height: 1.6;
            color: #1a1f2e;
        }

        /* Headings */
        h1 {
            color: #1a1f2e;
            border-bottom: 3px solid #007dc1;
            padding-bottom: 10px;
        }
        h2 {
            color: #1a1f2e;
            margin-top: 50px;
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 8px;
        }
        h3 { color: #333; margin-top: 30px; }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 10px 12px;
            text-align: left;
        }
        th {
            background: #f5f5f5;
            font-weight: 600;
        }
        tr:nth-child(even) { background: #fafafa; }

        /* Mermaid diagrams */
        .mermaid {
            background: #fafafa;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
        }

        /* Blockquotes for callouts */
        blockquote {
            border-left: 4px solid #007dc1;
            margin: 20px 0;
            padding: 10px 20px;
            background: #f0f7fc;
        }

        /* Discovery items */
        ul { padding-left: 25px; }
        li { margin: 8px 0; }

        /* Print button */
        .print-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #007dc1;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }
        .print-btn:hover { background: #0066a1; }

        /* Print styles */
        @media print {
            .print-btn { display: none !important; }
            body { padding: 0; font-size: 10pt; line-height: 1.35; }
            h2 { page-break-before: always; break-before: page; }
            h2:first-of-type { page-break-before: avoid; }
            h1, h2, h3, h4 { page-break-after: avoid; break-after: avoid; }
            .mermaid {
                page-break-inside: avoid;
                break-inside: avoid;
                max-width: 100%;
            }
            .mermaid svg { max-width: 100%; max-height: 500px; height: auto; }
            table { page-break-inside: avoid; font-size: 9pt; }
            p { orphans: 3; widows: 3; }
        }
    </style>
</head>
<body>

<!-- DOCUMENT CONTENT GOES HERE -->
<!-- Convert markdown headings to HTML -->
<!-- Convert mermaid code blocks to <div class="mermaid"> elements -->
<!-- Ensure <br> in mermaid blocks is NOT escaped to &lt;br&gt; -->

<button class="print-btn" onclick="window.print()">Print / Save as PDF</button>

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

**Critical HTML generation notes:**
- Mermaid code blocks MUST be `<div class="mermaid">` not `<pre><code>`
- HTML entities inside mermaid divs must NOT be escaped — `<br>` stays as `<br>`, not `&lt;br&gt;`
- Include `securityLevel: 'loose'` in mermaid init to allow HTML labels
- Include `curve: 'basis'` for smoother line routing
