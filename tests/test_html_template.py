#!/usr/bin/env python3
"""
Validate the HTML output template embedded in document-template.md.

Extracts the template, parses it with html.parser, and checks for
required structural elements that the styled output depends on.
"""
import re
from html.parser import HTMLParser
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent / "implementation-guide"
TEMPLATE_MD = SKILL_DIR / "references" / "document-template.md"


def extract_html_template():
    """Pull the html code block from document-template.md."""
    content = TEMPLATE_MD.read_text()
    match = re.search(r"```html\s*\n(.*?)\n```", content, re.DOTALL)
    assert match, "Could not find HTML code block in document-template.md"
    return match.group(1)


class TagBalanceChecker(HTMLParser):
    VOID_TAGS = {
        "br", "img", "hr", "meta", "input", "link", "area",
        "base", "col", "embed", "source", "track", "wbr",
    }

    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID_TAGS:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack:
            self.errors.append(f"Orphan closing tag </{tag}>")
        elif self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.errors.append(
                f"Tag mismatch: expected </{self.stack[-1]}>, got </{tag}>"
            )


def test_template_exists_and_extracts():
    html = extract_html_template()
    assert html.strip(), "HTML template extraction returned empty content"
    assert "<!DOCTYPE html>" in html, "Template missing DOCTYPE"


def test_template_html_is_balanced():
    html = extract_html_template()
    checker = TagBalanceChecker()
    checker.feed(html)
    assert not checker.errors, f"HTML tag balance errors: {checker.errors}"
    assert not checker.stack, f"Unclosed tags at end of template: {checker.stack}"


def test_template_has_mermaid_cdn():
    html = extract_html_template()
    assert "mermaid" in html.lower(), "Template missing mermaid reference"
    assert "cdn.jsdelivr.net" in html or "cdnjs" in html, \
        "Template missing mermaid CDN URL"


def test_template_has_mermaid_init():
    html = extract_html_template()
    assert "mermaid.initialize" in html, "Template missing mermaid.initialize call"
    assert "securityLevel" in html, "Template should set securityLevel"
    assert "curve" in html, "Template should set curve config"


def test_template_has_doc_header_class():
    html = extract_html_template()
    assert "doc-header" in html, "Template missing .doc-header element"
    assert "linear-gradient" in html, "Template missing gradient styling on header"


def test_template_has_all_four_callout_classes():
    html = extract_html_template()
    for variant in ["callout-info", "callout-warn", "callout-tip", "callout-danger"]:
        assert variant in html, f"Template missing callout class: {variant}"


def test_template_has_print_button():
    html = extract_html_template()
    assert "print-btn" in html, "Template missing .print-btn class"
    assert "window.print()" in html, "Template missing print() call"


def test_template_has_print_media_query():
    html = extract_html_template()
    assert "@media print" in html, "Template missing @media print rule"
    assert "page-break-inside" in html or "break-inside" in html, \
        "Template missing page-break-inside rule for mermaid/tables"


def test_template_has_h2_counter():
    html = extract_html_template()
    assert "counter-reset: section" in html, \
        "Template missing CSS counter-reset for section numbering"
    assert "counter-increment: section" in html, \
        "Template missing CSS counter-increment on h2"


def test_template_has_steps_pattern():
    html = extract_html_template()
    assert "steps" in html, "Template missing .steps class for numbered procedures"


def test_template_has_nav_path_pattern():
    html = extract_html_template()
    assert "nav-path" in html, "Template missing .nav-path class for UI breadcrumbs"


def test_template_has_discovery_panel():
    html = extract_html_template()
    assert "discovery" in html, "Template missing .discovery panel class"
