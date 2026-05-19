#!/usr/bin/env python3
"""
Run all skill validation tests. Exit 0 on success, 1 on any failure.

Usage: python tests/run_tests.py [--verbose]
"""
import sys
import importlib.util
from pathlib import Path

TESTS_DIR = Path(__file__).parent
TEST_MODULES = [
    "test_skill_structure",
    "test_mermaid_validator",
    "test_url_patterns",
    "test_review_fixtures",
    "test_html_template",
]


def load_module(name: str):
    path = TESTS_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_module(name: str, verbose: bool) -> tuple[int, int]:
    """Returns (passed, failed) for the module."""
    module = load_module(name)
    test_fns = [getattr(module, fn) for fn in dir(module) if fn.startswith("test_")]
    passed = 0
    failed = 0
    print(f"\n=== {name} ({len(test_fns)} tests) ===")
    for fn in test_fns:
        try:
            fn()
            passed += 1
            if verbose:
                print(f"  PASS  {fn.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL  {fn.__name__}: {e}")
        except Exception as e:
            failed += 1
            print(f"  ERROR {fn.__name__}: {type(e).__name__}: {e}")
    summary = f"{passed} passed, {failed} failed"
    print(f"  --- {summary}")
    return passed, failed


def main() -> int:
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    total_passed = 0
    total_failed = 0
    for name in TEST_MODULES:
        p, f = run_module(name, verbose)
        total_passed += p
        total_failed += f
    print(f"\n{'=' * 50}")
    print(f"TOTAL: {total_passed} passed, {total_failed} failed")
    print('=' * 50)
    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
