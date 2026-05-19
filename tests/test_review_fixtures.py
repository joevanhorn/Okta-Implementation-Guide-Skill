#!/usr/bin/env python3
"""
Validate the post-generation-review skill against a buggy-doc fixture
with intentional factual errors of each category.

This test confirms that the categories listed in post-generation-review.md
are recognizable by simple programmatic scanning, demonstrating they map
to detectable patterns. It does NOT replace Claude's actual review
reasoning — it validates the categorization is sound.
"""
import re
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent / "implementation-guide"
REVIEW_MD = SKILL_DIR / "references" / "post-generation-review.md"
FIXTURES = Path(__file__).parent / "fixtures"


def read_review():
    return REVIEW_MD.read_text()


def read_buggy_doc():
    return (FIXTURES / "buggy_implementation_guide.md").read_text()


def test_review_file_exists():
    assert REVIEW_MD.exists(), "post-generation-review.md must exist"


def test_review_declares_high_risk_categories():
    content = read_review()
    required_categories = [
        "Specification URIs",
        "Version numbers",
        "Count assertions",
        "Date-sensitive facts",
        "Default values",
        "UI menu paths",
        "Cross-document",
    ]
    for cat in required_categories:
        assert cat in content, \
            f"post-generation-review.md missing required category: {cat}"


def test_review_declares_procedure():
    content = read_review()
    required_steps = [
        "Inventory verifiable claims",
        "Classify each claim",
        "Verify",
        "Surface findings",
        "Apply fixes",
    ]
    for step in required_steps:
        assert step in content, \
            f"post-generation-review.md missing procedure step: {step}"


def test_review_specifies_no_severity_gradient():
    content = read_review()
    # Per project policy: all factual errors are equally serious. No Medium/Low tier.
    assert "equally serious" in content or "no Medium" in content.lower() or \
        "no medium or low" in content.lower(), \
        "post-generation-review.md must clarify all factual errors are equally serious"


def test_review_includes_parallel_section_strategy():
    content = read_review()
    assert "parallel" in content.lower() or "section" in content.lower(), \
        "post-generation-review.md should describe section-by-section strategy for large docs"
    # Specifically the 3000-line / 50-claim threshold
    assert "3000" in content or "50" in content, \
        "post-generation-review.md should give thresholds for splitting large docs"


def test_review_specifies_verified_despite_suspicion_pattern():
    content = read_review()
    assert "Verified" in content and "Suspicion" in content.lower() or \
        "verified despite suspicion" in content.lower(), \
        "post-generation-review.md must specify the 'verified despite suspicion' tracking pattern"


# --- Buggy doc fixture tests ---
# The buggy doc contains intentional errors of each category.
# We verify that simple regex scanning can find each error.
# This validates that the categories are programmatically recognizable.


def test_buggy_fixture_exists():
    assert (FIXTURES / "buggy_implementation_guide.md").exists(), \
        "Buggy implementation guide fixture must exist"


def test_buggy_fixture_contains_wrong_spec_uri():
    doc = read_buggy_doc()
    # Wrong SAML version in the persistent NameID format URI
    assert "urn:oasis:names:tc:SAML:1.1:nameid-format:persistent" in doc, \
        "Fixture should contain the wrong-SAML-version URI error"


def test_buggy_fixture_contains_count_assertion():
    doc = read_buggy_doc()
    # A count assertion that could be off-by-one
    assert re.search(r"\d+\s+commercial Regions", doc), \
        "Fixture should contain a count assertion"


def test_buggy_fixture_contains_version_number():
    doc = read_buggy_doc()
    # A specific version number that could be wrong
    assert re.search(r"\bv?\d+\.\d+(\.\d+)?\b", doc), \
        "Fixture should contain a specific version number"


def test_buggy_fixture_contains_ui_path():
    doc = read_buggy_doc()
    # A UI menu path that could be stale (look for separators)
    assert re.search(r"\w+\s*[>›]\s*\w+\s*[>›]\s*\w+", doc), \
        "Fixture should contain a UI menu path"
