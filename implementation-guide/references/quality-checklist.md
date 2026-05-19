# Quality Checklist

Run through this checklist before delivering any implementation guide. This is the final validation gate after Phase 5.5 (Review).

## Factual Accuracy

This section is the most important. All factual errors are equally serious — there is no Medium or Low tier for facts. Either every claim is correct, or the document does not ship.

- [ ] Phase 5.5.a (URL verification) was run, and every URL in the output appears in the verified list
- [ ] Phase 5.5.b (post-generation review) was run, and every factual claim has been classified VERIFIED or VERIFIED-IN-SESSION
- [ ] No claim remains in the TO CHECK state
- [ ] Findings list has been surfaced to the user and acknowledged
- [ ] All fixes have been applied and the file has been re-verified
- [ ] "Verified despite suspicion" list is documented for handoff

Common error categories the review must explicitly check:

- [ ] Specification URIs (SAML, OAuth, OIDC, WS-Fed, XML namespaces) — verified against the relevant standard
- [ ] Version numbers — verified against vendor release notes
- [ ] Count assertions ("N regions", "M factors", "K platforms") — recounted from the authoritative source
- [ ] Date-sensitive facts — verified against current vendor docs, not historical knowledge
- [ ] Default values (timeouts, ports, session durations) — verified against current product docs
- [ ] UI menu paths — verified against current vendor docs
- [ ] Cross-document contradictions (older vendor doc vs newer vendor doc) — explicitly handled, not silently picked

## Use Case Accuracy

- [ ] Every use case number matches the source document
- [ ] Every use case name matches the source document exactly (spelling, capitalization)
- [ ] Domain / scope annotations match the source document
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
- [ ] Line-break and bullet conventions follow current `mermaid-standards.md`
- [ ] No unescaped single quotes in node text
- [ ] Every `subgraph` has a matching `end`
- [ ] All referenced classes are defined with `classDef`
- [ ] All defined classes are assigned with `class` statements
- [ ] Brackets are balanced: `[]`, `{}`, `()`
- [ ] No overlapping line patterns (see `mermaid-standards.md` overlap prevention)
- [ ] Diagrams have max 12–15 nodes (split larger flows)

## HTML Output

- [ ] Mermaid code blocks are `<div class="mermaid">`, NOT `<pre><code>`
- [ ] HTML entities in mermaid blocks are NOT escaped (line breaks render, not `&lt;br&gt;`)
- [ ] Mermaid.js CDN script is included in `<head>`
- [ ] Mermaid init includes `securityLevel: 'loose'` and `curve: 'basis'`
- [ ] Print CSS prevents page breaks inside diagrams and tables
- [ ] Print CSS forces page breaks before `h2` elements
- [ ] Print / PDF button is present and functional
- [ ] Document uses the styled template (dark navy gradient header, CSS counter sections, callout boxes)
- [ ] All callout types render correctly (info, warn, tip, danger)

## Content Quality

- [ ] Platform component names are accurate (not guessed) — verified in Phase 5.5
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

## Verified Despite Suspicion — handoff record

Maintain a list of factual claims that looked suspicious during the review but were verified as correct against an authoritative source. Include this list when handing the document to the user. Purpose: future reviewers (or subsequent passes) should not re-litigate the same claims.

Format:

```
- Claim: [the specific claim text]
  Why it looked wrong: [what triggered suspicion]
  Why it's correct: [authoritative source and brief reason]
```

Common examples that have showed up in past reviews:

- The IAM trust policy `SAML:aud` condition checks the SAML response Destination, not the `<saml:Audience>` element, despite the name. This makes `SAML:aud = https://signin.aws.amazon.com/saml` correct even when the Okta Audience URI is `urn:amazon:webservices`.
- AWS WorkSpaces SAML supports Linux clients with year-based version strings like `2024.1` (Ubuntu 22.04) and `24.1` (Ubuntu 20.04). These look like typos but are the correct version format.
