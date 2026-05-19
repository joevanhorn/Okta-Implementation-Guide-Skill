# Post-Generation Review

The fabrication-hunting pass. Required step in Phase 5.5 of the skill workflow, after URL verification and before delivery.

## The rule

Every customer-facing document gets an untrusting review pass before delivery. Assume at least some factual claims are wrong. Verify each verifiable claim against an authoritative source.

This is not optional. Brand damage from a wrong fact in a delivered document is real and lasting.

## Why this exists

URL verification catches one specific class of error (broken citations). But Claude hallucinates many other things that URL verification does not catch:

- Specification URIs (SAML namespaces, OAuth scopes, XML namespace URLs)
- Version numbers, especially specific point releases
- Count assertions (number of supported regions, platforms, options)
- Date-sensitive facts that changed after the training cutoff
- Default values (timeouts, ports, session durations)
- UI menu paths in product consoles
- Cross-document consistency when two authoritative sources disagree

These slip past URL validation because they are not citations. The post-generation review pass is the discipline of explicitly hunting for them.

Real examples from production review passes:
- A doc claimed `urn:oasis:names:tc:SAML:1.1:nameid-format:persistent`. That URI does not exist — "persistent" was added in SAML 2.0. A customer pasting it into config would get an error.
- A doc claimed AWS WorkSpaces SAML is available in "15 commercial Regions." The actual count was 14.
- A doc listed an attribute as "Optional" that had become mandatory after the training cutoff (Microsoft KB5014754 strong-mapping requirement, September 2025).

Each of these is a credibility hit if shipped.

## When to run

After Phase 5 (Assemble) and after URL verification (Phase 5.5a), before Phase 6 (Deliver). The order matters:

1. Generate the document (Phase 4)
2. Assemble appendices and summary (Phase 5)
3. URL verification pass — see `url-verification.md`
4. **Post-generation review pass** — this file
5. Surface findings to the user
6. Apply fixes after acknowledgment
7. Re-verify any sections that were edited
8. Deliver (Phase 6)

## High-risk claim categories

The review must explicitly check each of these categories. They are listed in approximate order of frequency.

### Specification URIs

Any URI that looks like a standard namespace. Examples:
- SAML NameID format URIs (`urn:oasis:names:tc:SAML:2.0:nameid-format:*`)
- OAuth grant type URIs (`urn:ietf:params:oauth:grant-type:*`)
- OpenID Connect scope names
- WS-Federation namespace URIs
- XML schema URIs

For each one in the document: was it pasted from a verified source, or pattern-matched from memory? Pattern-matched URIs go to the verify list.

### Version numbers

Specific version strings: `5.20.0`, `2024.1`, `v3.4.2`. Marketing-rounded versions ("v5+" or "recent versions") are lower risk but should still be checked if specific.

For each one: verify against vendor release notes or product documentation in the same session.

### Count assertions

"Available in N regions." "Supports M client platforms." "K authentication factors."

Counts are easy to be wrong by one. Recount directly from the authoritative source — do not trust your own enumeration from memory.

### Date-sensitive facts

Things that changed after the training cutoff. The training cutoff is approximate, so the safe rule is: if a claim could plausibly have changed in the past two years, verify it.

Common triggers:
- "X is required as of [date]"
- "Y was deprecated in [version]"
- "Feature Z is now available in region W"
- Anything tied to compliance regulations or vendor security updates

### Default values

Timeouts, ports, session durations, retry counts, batch sizes. Vendors change defaults between versions. Stale defaults are a common error mode.

Verify against current product documentation, not historical knowledge.

### UI menu paths

Admin console navigation: `Settings > Security > Authentication > Policies`. Vendors restructure consoles frequently. A stale path looks like a typo to a customer trying to follow it.

Verify against current vendor documentation or screenshots in the same session.

### Cross-document contradictions

When two authoritative sources from the same vendor disagree, the document needs to handle the disagreement explicitly — not silently pick one source.

Common pattern: vendor's older docs say X, newer docs say Y, and both are still published. The review must catch when the document asserts X without acknowledging Y exists, or vice versa.

## The procedure

### Step 1: Inventory verifiable claims

Re-read the document in full. For each section, extract a list of verifiable factual claims into a working checklist. A verifiable claim is anything that can be checked against a primary source — a URI, version, count, date, default, path, or comparison.

For very large documents (more than ~50 verifiable claims, or more than ~3000 lines), split the document into sections and verify each section as a separate parallel task. Do not try to hold a 200-claim checklist in working memory.

### Step 2: Classify each claim

For each claim, mark one of:
- **VERIFIED** — pasted from a primary source fetched in this session
- **TO CHECK** — asserted from training-data memory, not yet verified
- **VERIFIED-IN-SESSION** — checked during step 3 below

### Step 3: Verify the "to check" claims

For each TO CHECK claim:
- Use `web_search` with `site:[vendor-domain]` to find the authoritative source
- Or use `web_fetch` if a direct URL is known
- Read the source — do not just look at search snippets
- Mark VERIFIED-IN-SESSION or FOUND-INCORRECT

For specification URIs: the OASIS, IETF, W3C, or vendor spec is authoritative. Other sites quoting the spec are secondary.

For vendor product claims: the vendor's current product documentation is authoritative. Blog posts, community forums, and third-party tutorials are secondary.

### Step 4: Surface findings

Before applying any fixes, present findings to the user. Format:

```
Found N factual errors and M items verified-as-correct-despite-suspicion.

ERRORS

#1. [Section / location]
    Currently: [what the doc says]
    Should be: [what the source says]
    Source:    [URL or doc reference]
    Why it's wrong: [one-line explanation]

#2. [Section / location]
    ...

VERIFIED DESPITE SUSPICION (informational — no fix needed)

- [Claim that looked wrong but is actually correct]
  Why I checked: [what made it look suspicious]
  Why it's right: [authoritative source said so]

- [Another such claim]
```

Wait for acknowledgment before fixing.

### Step 5: Apply fixes

After acknowledgment, apply each fix as a minimal targeted edit. Do not rewrite surrounding content beyond what is needed to incorporate the fix. After applying, re-verify the file is still well-formed and the fixes did not introduce new issues.

### Step 6: Re-deliver

Present the corrected document and the findings summary together. The findings summary serves two purposes: it shows the user what changed, and it documents the "verified despite suspicion" list so subsequent passes do not re-litigate the same claims.

## Severity

Per project policy, **all factual errors are equally serious for brand purposes**. There is no Medium or Low tier for factual claims. A wrong region count and a wrong spec URI are both errors that should not ship.

The only categorical distinction is:
- **ERROR** — a factually wrong claim that must be fixed before delivery
- **VERIFIED DESPITE SUSPICION** — informational; goes in the don't-re-litigate list

Style, clarity, and tone issues are out of scope for this review pass. The user discusses those per-document. This pass is strictly about factual accuracy.

## Parallel review for large documents

For documents larger than ~3000 lines or with more than ~50 verifiable claims:

1. Identify natural section boundaries (typically `<h2>` or major topic blocks)
2. Process each section as an independent review task — separate claim inventory, separate verification, separate findings
3. Merge findings into a single document-level report
4. Maintain a single "verified despite suspicion" list across sections to avoid duplicate re-checking

This approach also works well when the review is split across multiple sessions or sub-agents.

## What this review does not do

- Style or tone consistency — separate concern, user handles per document
- Grammar or typo checking — separate concern
- Architectural soundness of the proposed solution — that is the human's call, not Claude's
- Strategic positioning — that is the human's call

This pass is strictly about whether each verifiable factual claim is correct as stated.
