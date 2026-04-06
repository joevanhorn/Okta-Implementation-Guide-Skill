# Quality Checklist

Run through this checklist before delivering any implementation guide.

## Use Case Accuracy

- [ ] Every use case number matches the source document
- [ ] Every use case name matches the source document exactly (spelling, capitalization)
- [ ] Domain/scope annotations match the source document
- [ ] Every use case from the source appears in at least one section
- [ ] The Appendix A mapping accounts for ALL use cases

## Document Structure

- [ ] Executive Summary exists and includes use case count
- [ ] Every section has: Use Cases Covered, Overview, Mermaid diagram, Key Features table, Discovery Items
- [ ] Appendix A (Use Case Mapping) is complete
- [ ] Appendix B (Key Components) lists all platform components referenced
- [ ] Appendix C (Discovery Items Summary) consolidates all section-level items

## Mermaid Diagrams

- [ ] Every diagram starts with `flowchart TD`
- [ ] No `<br/>` anywhere (must be `<br>`)
- [ ] No `•` bullet characters (must be `-`)
- [ ] No unescaped single quotes in node text
- [ ] Every `subgraph` has a matching `end`
- [ ] All referenced classes are defined with `classDef`
- [ ] All defined classes are assigned with `class` statements
- [ ] Brackets are balanced: `[]`, `{}`, `()`
- [ ] No overlapping line patterns (see mermaid-standards.md overlap prevention)
- [ ] Diagrams have max 12-15 nodes (split larger flows)

## HTML Output

- [ ] Mermaid code blocks are `<div class="mermaid">`, NOT `<pre><code>`
- [ ] HTML entities in mermaid blocks are NOT escaped (`<br>` not `&lt;br&gt;`)
- [ ] Mermaid.js CDN script is included in `<head>`
- [ ] Mermaid init includes `securityLevel: 'loose'` and `curve: 'basis'`
- [ ] Print CSS prevents page breaks inside diagrams and tables
- [ ] Print CSS forces page breaks before `h2` elements
- [ ] Print/PDF button is present and functional

## Content Quality

- [ ] Platform component names are accurate (not guessed)
- [ ] Capabilities are not overstated — gaps are documented as discovery items
- [ ] Discovery items are specific and actionable, not vague
- [ ] Each section's overview explains the business problem, not just the technical flow
- [ ] Feature tables include WHY each feature matters, not just what it does

## Mermaid Syntax Validation

If you have access to code execution, validate diagrams programmatically:

```python
import re

def validate_mermaid(code):
    issues = []

    if not code.strip().startswith('flowchart'):
        issues.append("Missing flowchart declaration")

    for open_char, close_char in [('[', ']'), ('{', '}'), ('(', ')')]:
        if code.count(open_char) != code.count(close_char):
            issues.append(f"Unbalanced {open_char}{close_char}")

    subgraph_count = len(re.findall(r'subgraph\s', code))
    end_count = len(re.findall(r'^\s*end\s*$', code, re.MULTILINE))
    if subgraph_count != end_count:
        issues.append(f"Subgraph mismatch: {subgraph_count} subgraphs, {end_count} ends")

    if '<br/>' in code:
        issues.append("Found <br/> — use <br> instead")
    if '•' in code:
        issues.append("Found bullet character — use - instead")

    class_defs = set(re.findall(r'classDef\s+(\w+)', code))
    class_uses = set()
    for match in re.findall(r'class\s+([\w,]+)\s+(\w+)', code):
        class_uses.add(match[1])
    
    undefined = class_uses - class_defs
    if undefined:
        issues.append(f"Classes used but not defined: {undefined}")
    
    unused = class_defs - class_uses
    if unused:
        issues.append(f"Classes defined but not used: {unused}")

    return issues
```

Run this against every mermaid block before delivering. Fix any issues found.
