#!/usr/bin/env python3
"""
Keep the behavioral routing evals honest:
- the scenario fixtures must reference real product files, and
- the committed baseline run (results.sample.json) must still grade 10/10.

The agent-driven "actor" step lives outside CI (see evals/README.md); this module
guards the deterministic grader + fixtures so a skill change that would break routing
expectations, or a fixture that drifts from disk, fails the suite.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
EVALS_DIR = ROOT / "evals"
REFS_DIR = ROOT / "implementation-guide" / "references"


def _load(name):
    return json.loads((EVALS_DIR / name).read_text())


def test_eval_fixtures_reference_real_files():
    spec = _load("routing_scenarios.json")
    for f in spec["product_keywords"]:
        assert (REFS_DIR / f).exists(), f"product_keywords names a missing file: {f}"
    for scn in spec["scenarios"]:
        for f in scn["expected_products"]:
            assert (REFS_DIR / f).exists(), \
                f"scenario {scn['id']} expects a missing file: {f}"


def test_every_product_file_has_a_scenario():
    """Each product reference file should be exercised by at least one eval scenario."""
    spec = _load("routing_scenarios.json")
    covered = set()
    for scn in spec["scenarios"]:
        covered.update(scn["expected_products"])
    product_files = {p.name for p in REFS_DIR.glob("*-reference.md")}
    uncovered = product_files - covered
    assert not uncovered, f"product reference files with no eval scenario: {uncovered}"


def test_sample_results_grade_all_pass():
    """The committed baseline run must still grade 10/10 (guards the grader + fixtures)."""
    sys.path.insert(0, str(EVALS_DIR))
    import grade  # noqa: E402

    spec = _load("routing_scenarios.json")
    product_keywords = spec["product_keywords"]
    adjacencies = spec.get("adjacencies", {})
    results = _load("results.sample.json")["results"]
    failures = []
    for scn in spec["scenarios"]:
        result = results.get(scn["id"])
        assert result is not None, f"sample results missing scenario: {scn['id']}"
        ok, reasons = grade.grade_scenario(scn, result, product_keywords, adjacencies)
        if not ok:
            failures.append((scn["id"], reasons))
    assert not failures, f"baseline eval run no longer passes: {failures}"
