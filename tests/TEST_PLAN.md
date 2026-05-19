# Skill Validation Test Plan

Automated tests that Claude Code can run to validate the `implementation-guide` skill after any change. Designed to be run independently — no human in the loop, no external test framework, fast execution.

## Run

From the repo root:

```bash
python tests/run_tests.py
```

Or to run a specific test module:

```bash
python tests/test_skill_structure.py
python tests/test_mermaid_validator.py
python tests/test_url_patterns.py
python tests/test_review_fixtures.py
python tests/test_html_template.py
```

Exit code 0 = all tests pass. Non-zero = at least one failure.

## What the tests cover

### 1. Skill structure (`test_skill_structure.py`)

Validates the skill file layout and content invariants:

- All required files exist under `implementation-guide/`
- `SKILL.md` has the required frontmatter fields (`name`, `description`)
- `SKILL.md` declares all phases (1, 2, 3, 4, 5, 5.5, 6)
- The "Before Starting" reference table in `SKILL.md` lists every file in `references/`
- Every file listed in the reference table actually exists
- Every reference file is non-empty and starts with an `# Title` heading

### 2. Mermaid validator (`test_mermaid_validator.py`)

Runs the validator function from `quality-checklist.md` against curated fixtures:

- Known-good diagrams pass with zero issues
- Known-bad diagrams trigger the expected error
- Each error category in the validator is exercised by at least one fixture

Fixtures in `tests/fixtures/mermaid/`:

- `good_simple.txt`, `good_with_subgraph.txt` — should produce no errors
- `bad_unbalanced_brackets.txt` — unbalanced `[` count
- `bad_subgraph_no_end.txt` — subgraph without matching `end`
- `bad_bullet_char.txt` — uses `•` instead of `-`
- `bad_undefined_class.txt` — `class` reference without matching `classDef`
- `bad_unused_classdef.txt` — `classDef` without matching `class` reference

### 3. URL patterns (`test_url_patterns.py`)

Scans the URL-verification reference for the known fabrication patterns table, then verifies a detector function would flag URLs matching those patterns:

- Each row in the "AI-generated path / Actual path" table becomes a test case
- Given a candidate URL matching the AI-generated pattern, the detector flags it
- Given a candidate URL matching the actual pattern, the detector does not flag it

This is a policy check, not a live URL check. Live URL verification requires network access and is not part of the deterministic test suite.

### 4. Review pass fixtures (`test_review_fixtures.py`)

Validates the post-generation-review skill against a "buggy doc" fixture that contains intentional factual errors of each category:

- Wrong spec URI (`urn:oasis:names:tc:SAML:1.1:nameid-format:persistent` — should be 2.0)
- Wrong version number
- Off-by-one count
- Stale UI menu path

The test confirms the review-finding regex extractor can identify each error in the document. This validates the review *output format*, not Claude's reasoning — a heuristic check that the doc-scanning tooling could plausibly catch the kinds of issues the review should surface.

### 5. HTML template (`test_html_template.py`)

Extracts the HTML template from `document-template.md` and validates:

- HTML parses cleanly with `html.parser`
- All opened tags have matching close tags (or are void elements)
- Required structural elements present: `.doc-header`, `.print-btn`, mermaid CDN `<script>`, mermaid init `<script>`
- CSS selectors for all four callout types present (info, warn, tip, danger)
- Print media query present
- CSS counter rules for h2 numbering present

## When to re-run

Run the full test suite:

- After any change to `SKILL.md`
- After any change to files in `references/`
- After any change to `assets/`
- Before tagging a release
- In CI on every pull request (recommended GitHub Actions workflow below)

## CI integration (suggested)

Add to `.github/workflows/test.yml`:

```yaml
name: Validate Skill
on:
  push:
    branches: [master, main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: python tests/run_tests.py
```

No additional dependencies — the test suite uses only the Python standard library.

## Adding tests

When the skill grows new capabilities, add tests in this order:

1. Add a fixture under `tests/fixtures/` representing the new behavior
2. Add a test function in the appropriate `test_*.py` module
3. Run the test in isolation to confirm it fails (then passes after the skill change)
4. Re-run the full suite to confirm no regressions

When new URL fabrication patterns are added to `url-verification.md`, mirror the row in `test_url_patterns.py`.
