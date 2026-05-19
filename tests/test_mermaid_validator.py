#!/usr/bin/env python3
"""
Validate the mermaid validator function from quality-checklist.md.

Loads the validator definition from the reference file, then runs it
against curated fixtures to verify each rule catches what it should.
"""
import re
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent / "implementation-guide"
FIXTURES = Path(__file__).parent / "fixtures" / "mermaid"


def load_validator():
    """Extract the validate_mermaid function from quality-checklist.md and exec it."""
    content = (SKILL_DIR / "references" / "quality-checklist.md").read_text()
    # Find the python code block defining validate_mermaid
    match = re.search(
        r"```python\s*\n(import re\s*\n.*?def validate_mermaid.*?)```",
        content,
        re.DOTALL,
    )
    assert match, "Could not find validate_mermaid in quality-checklist.md"
    namespace = {}
    exec(match.group(1), namespace)
    return namespace["validate_mermaid"]


def read_fixture(name: str) -> str:
    return (FIXTURES / name).read_text()


def test_validator_loads():
    fn = load_validator()
    assert callable(fn)


def test_good_simple_passes():
    fn = load_validator()
    issues = fn(read_fixture("good_simple.txt"))
    assert issues == [], f"Good fixture should pass, got: {issues}"


def test_good_with_subgraph_passes():
    fn = load_validator()
    issues = fn(read_fixture("good_with_subgraph.txt"))
    assert issues == [], f"Good fixture with subgraph should pass, got: {issues}"


def test_unbalanced_brackets_caught():
    fn = load_validator()
    issues = fn(read_fixture("bad_unbalanced_brackets.txt"))
    assert any("Unbalanced" in i for i in issues), \
        f"Should catch unbalanced brackets, got: {issues}"


def test_subgraph_no_end_caught():
    fn = load_validator()
    issues = fn(read_fixture("bad_subgraph_no_end.txt"))
    assert any("Subgraph mismatch" in i for i in issues), \
        f"Should catch subgraph without end, got: {issues}"


def test_bullet_char_caught():
    fn = load_validator()
    issues = fn(read_fixture("bad_bullet_char.txt"))
    assert any("bullet character" in i for i in issues), \
        f"Should catch bullet character, got: {issues}"


def test_undefined_class_caught():
    fn = load_validator()
    issues = fn(read_fixture("bad_undefined_class.txt"))
    assert any("used but not defined" in i for i in issues), \
        f"Should catch undefined class, got: {issues}"


def test_unused_classdef_caught():
    fn = load_validator()
    issues = fn(read_fixture("bad_unused_classdef.txt"))
    assert any("defined but not used" in i for i in issues), \
        f"Should catch unused classDef, got: {issues}"


def test_missing_flowchart_declaration_caught():
    fn = load_validator()
    code = "Start --> End\nclassDef foo fill:#fff\nclass Start foo\nclass End foo"
    issues = fn(code)
    assert any("flowchart" in i.lower() for i in issues), \
        f"Should catch missing flowchart declaration, got: {issues}"
