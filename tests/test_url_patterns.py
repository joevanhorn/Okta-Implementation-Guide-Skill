#!/usr/bin/env python3
"""
Validate that url-verification.md documents the known fabrication patterns
and that the file structure supports the workflow described in SKILL.md.

This is a policy check, not a live URL check — live URL verification
requires network access and is excluded from the deterministic suite.
"""
import re
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent / "implementation-guide"
URL_VERIFICATION_MD = SKILL_DIR / "references" / "url-verification.md"


def read_url_verification():
    return URL_VERIFICATION_MD.read_text()


def test_url_verification_file_exists():
    assert URL_VERIFICATION_MD.exists(), "url-verification.md must exist"


def test_states_the_rule_clearly():
    content = read_url_verification()
    assert "must be verified" in content.lower(), \
        "url-verification.md must state the verification rule"


def test_anti_extrapolation_warning_present():
    content = read_url_verification()
    # The critical anti-pattern: extrapolating from sibling URLs
    assert "extrapolat" in content.lower(), \
        "url-verification.md must warn against extrapolation"
    assert "SAML" in content and "OIDC" in content, \
        "url-verification.md must include the SAML vs OIDC counter-example"


def test_domain_risk_table_present():
    content = read_url_verification()
    # The risk classification table
    assert "help.okta.com" in content, "Risk table must include help.okta.com"
    assert "HIGH" in content, "Risk table must include HIGH risk classification"
    assert "LOW" in content, "Risk table must include LOW risk classification"


def test_help_okta_anti_patterns_table_present():
    content = read_url_verification()
    # The structural anti-patterns table should have at least 5 known rows
    # Each row is an example of an AI-generated path vs actual path
    known_anti_patterns = [
        "api-config",          # AI generates /api-access-management/, actual is api-config-
        "identity-engine",     # AI generates /security/authenticators/, actual is /identity-engine/
        "branding-pages",      # Custom sign-in lives at branding-pages.htm
        "settings-configure",  # Settings have settings-configure- prefix
    ]
    for marker in known_anti_patterns:
        assert marker in content, \
            f"url-verification.md missing known anti-pattern marker: {marker}"


def test_verification_methods_enumerated():
    content = read_url_verification()
    assert "web_fetch" in content, "Must reference web_fetch as verification method"
    assert "web_search" in content, "Must reference web_search as verification method"
    assert "site:" in content, "Must reference site: search operator"


def test_what_verified_does_not_mean_section():
    content = read_url_verification()
    # The "verified does not mean" section catches subtle gotchas
    assert "not verified" in content.lower() or "is NOT verified" in content, \
        "url-verification.md should explicitly list what NOT verified means"


def test_workflow_distinguishes_generation_vs_final_pass():
    content = read_url_verification()
    assert "during generation" in content.lower(), \
        "url-verification.md should describe URL discipline during generation"
    assert "final pass" in content.lower() or "before delivery" in content.lower(), \
        "url-verification.md should describe the final verification pass"
