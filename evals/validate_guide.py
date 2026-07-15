#!/usr/bin/env python3
"""
Validate a generated implementation guide (markdown) against the skill's own output
contract — the structure required by references/document-template.md — and run the
repo's own validate_mermaid (from quality-checklist.md) on every diagram.

This is the checker half of the generation smoke test: an agent runs the skill
end-to-end to produce a guide (see evals/README.md), and this script confirms the
deliverable actually has the required shape and valid diagrams.

Usage:
    python3 evals/validate_guide.py <guide.md> [<guide2.md> ...]

Exit 0 iff every guide passes.
"""
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent / "implementation-guide"


def load_validator():
    """Reuse the validate_mermaid function defined in quality-checklist.md."""
    content = (SKILL_DIR / "references" / "quality-checklist.md").read_text()
    match = re.search(
        r"```python\s*\n(import re\s*\n.*?def validate_mermaid.*?)```",
        content,
        re.DOTALL,
    )
    if not match:
        raise RuntimeError("Could not find validate_mermaid in quality-checklist.md")
    namespace = {}
    exec(match.group(1), namespace)
    return namespace["validate_mermaid"]


MERMAID_BLOCK = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)
TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$", re.MULTILINE)


def validate_guide(path: Path, validate_mermaid) -> list[str]:
    text = path.read_text()
    problems = []

    # --- top-level structure ---
    if "## Executive Summary" not in text:
        problems.append("missing '## Executive Summary'")
    for appx in ("Appendix A", "Appendix B", "Appendix C"):
        if appx not in text:
            problems.append(f"missing '{appx}'")

    # --- sections (each carries a 'Use Cases Covered' marker) ---
    markers = [m.start() for m in re.finditer(r"Use Cases Covered", text)]
    n_sections = len(markers)
    if n_sections < 3:
        problems.append(f"expected >=3 sections, found {n_sections} (by 'Use Cases Covered')")

    # Per-section element checks. Bound each section at the next marker, or at the
    # first appendix/executive-summary heading, whichever comes first.
    tail_start = min(
        [text.find(h) for h in ("## Appendix A", "## Executive Summary") if text.find(h) >= 0]
        or [len(text)]
    )
    bounds = markers + [len(text)]
    for i, start in enumerate(markers):
        end = bounds[i + 1]
        if start < tail_start:
            end = min(end, tail_start) if end > tail_start else end
        chunk = text[start:end]
        label = f"section {i + 1}"
        if not MERMAID_BLOCK.search(chunk):
            problems.append(f"{label}: no ```mermaid diagram")
        if not TABLE_ROW.search(chunk):
            problems.append(f"{label}: no key-features table")
        if "Discovery Item" not in chunk and "Discovery item" not in chunk:
            problems.append(f"{label}: no Discovery Items")

    # --- mermaid validity (repo's own validator) ---
    diagrams = MERMAID_BLOCK.findall(text)
    if len(diagrams) < n_sections:
        problems.append(f"expected >=1 diagram per section ({n_sections}), found {len(diagrams)}")
    for j, dia in enumerate(diagrams, 1):
        issues = validate_mermaid(dia)
        for issue in issues:
            problems.append(f"diagram {j}: {issue}")

    return problems


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: validate_guide.py <guide.md> [...]")
        return 2
    validate_mermaid = load_validator()
    all_ok = True
    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.exists():
            print(f"  MISSING  {arg}")
            all_ok = False
            continue
        diagrams = len(MERMAID_BLOCK.findall(path.read_text()))
        sections = len(re.findall(r"Use Cases Covered", path.read_text()))
        problems = validate_guide(path, validate_mermaid)
        if problems:
            all_ok = False
            print(f"  FAIL  {path.name}  ({sections} sections, {diagrams} diagrams)")
            for p in problems:
                print(f"          - {p}")
        else:
            print(f"  PASS  {path.name}  ({sections} sections, {diagrams} diagrams)")
    print("=" * 50)
    print("ALL GUIDES PASS" if all_ok else "SOME GUIDES FAILED")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
