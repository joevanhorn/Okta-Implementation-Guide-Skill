#!/usr/bin/env python3
"""
Validate skill file layout and content invariants.
"""
import re
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent / "implementation-guide"

REQUIRED_FILES = [
    "SKILL.md",
    "references/mermaid-standards.md",
    "references/document-template.md",
    "references/url-verification.md",
    "references/post-generation-review.md",
    "references/quality-checklist.md",
    "references/okta-oig-reference.md",
    "references/research-protocol.md",
    "assets/renderer.html",
]


def test_all_required_files_exist():
    for rel in REQUIRED_FILES:
        path = SKILL_DIR / rel
        assert path.exists(), f"Missing required file: {rel}"


def test_skill_md_has_frontmatter():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    assert skill.startswith("---\n"), "SKILL.md must start with frontmatter delimiter"
    end_marker = skill.find("\n---\n", 4)
    assert end_marker > 0, "SKILL.md frontmatter not terminated"
    frontmatter = skill[4:end_marker]
    assert re.search(r"^name:\s*\S+", frontmatter, re.MULTILINE), \
        "SKILL.md frontmatter missing `name`"
    assert re.search(r"^description:\s*\S+", frontmatter, re.MULTILINE), \
        "SKILL.md frontmatter missing `description`"


def test_skill_md_declares_all_phases():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    required_phases = [
        "## Phase 1:",
        "## Phase 2:",
        "## Phase 3:",
        "## Phase 4:",
        "## Phase 5:",
        "## Phase 5.5:",
        "## Phase 6:",
    ]
    for phase in required_phases:
        assert phase in skill, f"SKILL.md missing phase declaration: {phase}"


def test_skill_md_reference_table_matches_files():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    # Find all `references/foo.md` references in the SKILL.md reference table
    referenced = set(re.findall(r"`references/([\w-]+\.md)`", skill))
    actual = set(p.name for p in (SKILL_DIR / "references").glob("*.md"))
    missing_in_table = actual - referenced
    missing_in_dir = referenced - actual
    assert not missing_in_table, \
        f"Files exist in references/ but not listed in SKILL.md table: {missing_in_table}"
    assert not missing_in_dir, \
        f"Files referenced in SKILL.md table but missing on disk: {missing_in_dir}"


def test_reference_files_nonempty_with_heading():
    for ref in (SKILL_DIR / "references").glob("*.md"):
        content = ref.read_text().strip()
        assert content, f"Empty reference file: {ref.name}"
        first_line = content.split("\n", 1)[0]
        assert first_line.startswith("# "), \
            f"Reference file does not start with `# Title`: {ref.name} (got: {first_line!r})"


def test_skill_md_has_review_phase_with_subpasses():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    assert "5.5.a" in skill or "URL verification pass" in skill, \
        "SKILL.md Phase 5.5 must declare a URL verification sub-pass"
    assert "5.5.b" in skill or "fact-checking review" in skill or \
        "post-generation" in skill.lower(), \
        "SKILL.md Phase 5.5 must declare a post-generation review sub-pass"


def test_honest_principle_present():
    skill = (SKILL_DIR / "SKILL.md").read_text()
    # The "Honest, not impressive" principle should be in the Key Principles section
    assert re.search(r"honest.*not.*impressive", skill, re.IGNORECASE), \
        "SKILL.md should declare the 'Honest, not impressive' principle"
