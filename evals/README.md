# Behavioral Routing Evals

The `tests/` suite validates the skill's **structure** (files exist, tables stay in
sync, templates are followed). These evals validate its **behavior**: given a realistic
request, does an agent following `SKILL.md` route to the right product reference file(s),
disambiguate when the product is unnamed, handle multi-product opportunities, and hold
the "Honest, not impressive" line under pressure?

Because the "skill" is instructions (not executable code), the eval has two halves:

1. **Actor step (agent-driven).** For each scenario, a fresh agent reads `SKILL.md`
   (plus the referenced files) and returns a routing *decision* as JSON — which
   reference file(s) it would load, whether it would pause to clarify, which product(s)
   it recommends, and any honesty/currency caveats it would surface. Fresh context per
   scenario mirrors a real, independent skill invocation.
2. **Grader step (deterministic).** `grade.py` scores those captured decisions against
   the expectations in `routing_scenarios.json`. Reproducible and CI-checkable.

## Files

| File | Purpose |
|------|---------|
| `routing_scenarios.json` | 10 scenarios: prompt + expected product file(s), clarification expectation, and required honesty/currency flag groups. Also holds `product_keywords` used for matching. |
| `results.sample.json` | Captured actor decisions from the reference run (10/10 pass). The committed baseline. |
| `grade.py` | Scores a results file against the scenarios. Exit 0 iff all pass. |

## Running the actor step

Run each scenario as its own agent (Claude Code Task / Agent tool, `claude -p`, or the
API). Give the agent only the prompt and the skill files — **never** the expected answer.
Prompt template:

> You are simulating the "implementation-guide" skill to test its ROUTING behavior.
> Read `implementation-guide/SKILL.md` and
> `implementation-guide/references/product-portfolio-map.md`. Following the skill's
> routing / disambiguation / portfolio-scoping logic, decide how to handle this request
> (do NOT generate a guide or run web searches). Output ONLY a JSON block:
> `{ "reference_files": [...], "will_ask_clarification": bool, "recommended_products": [...], "notable_flags": "..." }`
>
> USER REQUEST: "<scenario prompt>"

For the honesty/currency scenarios (`honest-opa-cyberark`, `auth0-currency`), point the
agent at the relevant product reference file too, and ask it to include the caveats it
would surface.

Collect each agent's JSON into a results file keyed by scenario `id` (see
`results.sample.json` for the shape), then grade:

```bash
python3 evals/grade.py path/to/results.json
# or, against the committed baseline:
python3 evals/grade.py
```

## Scoring

Each scenario must pass four checks:

- **routing** — expected product file(s) loaded, or (when the product is unnamed and the
  agent defers loading) named in `recommended_products`. An intentionally ambiguous
  scenario must load **no** product file.
- **no_wrong** — no unexpected product file loaded.
- **clarification** — `will_ask_clarification` matches when the scenario enforces it
  (`clarification_expected` true/false; `null` = not enforced).
- **flags** — every `required_flag_group` appears in `notable_flags` (each group is a set
  of synonyms; at least one must appear).

## What the baseline run demonstrates

- Correct single-product routing across all eight product families.
- **Disambiguation:** the bare `"an implementation guide for Okta"` request refuses to
  guess a product and asks for clarification.
- **Multi-product:** an opportunity spanning SSO + privileged access + access reviews
  loads WIC + OPA + OIG together.
- **Honesty under pressure:** a request to "confirm OPA fully replaces CyberArk" for
  mainframe / network devices / databases surfaces those as native gaps instead of
  overstating parity.
- **Product currency:** an Auth0 Rules/Hooks request flags the Nov 18 2026 sunset and
  recommends migrating to Actions.

## Generation smoke test

The routing evals stop at Phase 3 (which reference file gets loaded). The **generation
smoke test** goes all the way: an agent runs the skill end-to-end (Direct Mode, real
Phase 3 current-state web validation, Phase 4 generation, Phase 5 appendices, Phase 5.5
review) to produce a complete guide, and `validate_guide.py` checks the deliverable
against the skill's own output contract.

- **Actor step:** run the skill for a fully-specified engagement (customer, platform,
  use cases) and save the result to `evals/smoke/<slug>-implementation-guide.md`.
- **Checker step:** `python3 evals/validate_guide.py evals/smoke/*.md` — verifies each
  guide has an Executive Summary, Appendices A/B/C, ≥3 sections each carrying all five
  required elements (Use Cases Covered, overview, one `mermaid` diagram, a key-features
  table, discovery items), one diagram per section, and that **every diagram passes the
  repo's own `validate_mermaid`** (reused from `quality-checklist.md`).

`evals/smoke/` holds three committed reference guides — Auth0 CIC, Okta Device Access,
and Okta Access Gateway — that pass the contract and are also checked in CI
(`test_evals.py::test_smoke_guides_validate`). They double as worked examples of the
skill's output, including its honest-framing behavior under real generation (the Auth0
guide surfaces the Nov 2026 Rules/Hooks sunset; Device Access states the no-Linux/no-RDP
scope limits; Access Gateway frames OAG as a migration bridge, not a target state).

## Re-running after a change

Any time you change routing logic, the portfolio map, or a product reference file:
re-run the actor step, capture fresh results, and grade. If a scenario regresses, the
grader names the failing dimension and reason.
