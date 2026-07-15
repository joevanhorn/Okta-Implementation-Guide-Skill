#!/usr/bin/env python3
"""
Grade behavioral routing-eval results against expected outcomes.

The eval "actor" step is agent-driven (a fresh Claude agent simulates the skill on
each scenario and returns a routing decision as JSON — see README.md). This grader is
the deterministic half: it scores those captured decisions so a run is reproducible and
CI-checkable.

Usage:
    python3 evals/grade.py [results.json]

Defaults to evals/results.sample.json (the committed reference run). Exit 0 if every
scenario passes, 1 otherwise.

Scoring dimensions per scenario:
  routing         expected product reference file(s) loaded, OR (when the product is
                  unnamed and the agent defers loading) the product is named in
                  recommended_products. For an intentionally ambiguous scenario
                  (expected_products == []), the agent must NOT commit to any product.
  no_wrong        no unexpected product reference file was loaded.
  clarification   will_ask_clarification matches when the scenario enforces it
                  (clarification_expected is true/false; null = not enforced).
  flags           every required_flag_group is represented in notable_flags
                  (honesty caveats / product-currency warnings the skill should surface).
"""
import json
import sys
from pathlib import Path

EVALS_DIR = Path(__file__).parent
NON_PRODUCT_FILES = {"product-portfolio-map.md"}


def basename(f: str) -> str:
    return f.rsplit("/", 1)[-1].strip()


def grade_scenario(scn: dict, result: dict, product_keywords: dict, adjacencies: dict = None) -> tuple[bool, list[str]]:
    reasons = []
    ref_files = {basename(f) for f in result.get("reference_files", [])}
    product_refs = ref_files - NON_PRODUCT_FILES
    recommended = " ".join(result.get("recommended_products", []) or []).lower()
    notable = (result.get("notable_flags") or "").lower()
    expected = list(scn.get("expected_products", []))

    # --- routing ---
    if not expected:
        routing_ok = len(product_refs) == 0
        if not routing_ok:
            reasons.append(f"routing: expected no product commitment, but loaded {sorted(product_refs)}")
    else:
        missing = []
        for exp in expected:
            covered = exp in ref_files or any(kw in recommended for kw in product_keywords.get(exp, []))
            if not covered:
                missing.append(exp)
        routing_ok = not missing
        if missing:
            reasons.append(f"routing: expected product(s) not covered: {missing}")

    # --- no wrong product ---
    # Allow the expected product(s) plus their portfolio-map "also consider" adjacencies;
    # a cross-domain co-load is still a failure.
    adjacencies = adjacencies or {}
    allowed = set(expected)
    for exp in expected:
        allowed.update(adjacencies.get(exp, []))
    wrong = product_refs - allowed
    no_wrong = not wrong
    if wrong:
        reasons.append(f"no_wrong: unexpected product file(s) loaded: {sorted(wrong)}")

    # --- clarification ---
    clar_expected = scn.get("clarification_expected", None)
    if clar_expected is None:
        clarification_ok = True
    else:
        clarification_ok = bool(result.get("will_ask_clarification")) == bool(clar_expected)
        if not clarification_ok:
            reasons.append(
                f"clarification: expected will_ask_clarification={clar_expected}, "
                f"got {result.get('will_ask_clarification')}"
            )

    # --- flags ---
    flags_ok = True
    for group in scn.get("required_flag_groups", []):
        if not any(syn.lower() in notable for syn in group):
            flags_ok = False
            reasons.append(f"flags: none of {group} found in notable_flags")

    passed = routing_ok and no_wrong and clarification_ok and flags_ok
    return passed, reasons


def main() -> int:
    scenarios_path = EVALS_DIR / "routing_scenarios.json"
    results_path = Path(sys.argv[1]) if len(sys.argv) > 1 else EVALS_DIR / "results.sample.json"

    spec = json.loads(scenarios_path.read_text())
    product_keywords = spec.get("product_keywords", {})
    adjacencies = spec.get("adjacencies", {})
    scenarios = spec["scenarios"]
    results = json.loads(results_path.read_text()).get("results", {})

    print(f"Grading {results_path.name} against {len(scenarios)} scenarios\n")
    passed_count = 0
    failed = []
    for scn in scenarios:
        sid = scn["id"]
        result = results.get(sid)
        if result is None:
            print(f"  FAIL  {sid}: no result captured")
            failed.append(sid)
            continue
        ok, reasons = grade_scenario(scn, result, product_keywords, adjacencies)
        if ok:
            print(f"  PASS  {sid}")
            passed_count += 1
        else:
            print(f"  FAIL  {sid}")
            for r in reasons:
                print(f"          - {r}")
            failed.append(sid)

    print(f"\n{'=' * 50}")
    print(f"TOTAL: {passed_count}/{len(scenarios)} scenarios passed")
    print('=' * 50)
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
