"""Negative tests — verify that intentionally broken code is caught by checks.

Two types:
- must_fail: Check MUST catch this mutation. Test FAILs if check passes.
- should_fail: Check SHOULD catch this, but might not (blind spot discovery).
  Test always passes, but results are collected for the precision report.
"""

import importlib.util
from pathlib import Path

import pytest

CASES_DIR = Path(__file__).parent.parent / "cases"


def _run_checks_on_code(case_dir: Path, code: str):
    """Run all check modules on code, return list of CheckDetails."""
    all_details = []
    for module_name in ("static", "behavior"):
        check_file = case_dir / "checks" / f"{module_name}.py"
        if not check_file.exists():
            continue
        module_key = f"{case_dir.name}.{module_name}"
        spec = importlib.util.spec_from_file_location(module_key, check_file)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        details = mod.run_checks(code)
        all_details.extend(details)
    return all_details


def _discover(field: str):
    """Find all negatives with the given field (must_fail or should_fail).

    Cases live at cases/<sdk>/<case>/ (current) or cases/<case>/ (legacy
    flat layout) — glob both levels so neither is silently skipped.
    """
    neg_files = sorted(
        list(CASES_DIR.glob("*/checks/negatives.py"))
        + list(CASES_DIR.glob("*/*/checks/negatives.py"))
    )
    items = []
    for neg_file in neg_files:
        case_dir = neg_file.parent.parent
        spec = importlib.util.spec_from_file_location(f"neg.{case_dir.name}", neg_file)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for neg in getattr(mod, "NEGATIVES", []):
            if field in neg:
                items.append((case_dir, neg))
    return items


# === must_fail tests (strict — test fails if check doesn't catch it) ===

MUST_FAIL_ITEMS = _discover("must_fail")


@pytest.mark.parametrize(
    "case_dir,negative",
    MUST_FAIL_ITEMS,
    ids=[f"{cdir.name}-{neg['name']}" for cdir, neg in MUST_FAIL_ITEMS],
)
def test_negative_detected(case_dir: Path, negative: dict) -> None:
    """Mutated code must fail the specified checks."""
    case_id = case_dir.name
    ref_code = (case_dir / "reference" / "main.c").read_text(encoding="utf-8")
    bad_code = negative["mutation"](ref_code)
    assert bad_code != ref_code, f"Mutation '{negative['name']}' did not change the code"

    all_details = _run_checks_on_code(case_dir, bad_code)

    for check_name in negative["must_fail"]:
        matching = [d for d in all_details if d.check_name == check_name]
        assert matching, f"Check '{check_name}' not found in any module for {case_id}"
        assert all(not d.passed for d in matching), (
            f"Check '{check_name}' should FAIL on mutation '{negative['name']}' "
            f"but at least one PASSED. results={[(d.passed, d.actual) for d in matching]}"
        )


# === should_fail tests (discovery — always passes, reports blind spots) ===

SHOULD_FAIL_ITEMS = _discover("should_fail")

# Collect results for the precision report
BLIND_SPOTS: list[dict] = []


@pytest.mark.parametrize(
    "case_dir,negative",
    SHOULD_FAIL_ITEMS,
    ids=[f"subtle-{cdir.name}-{neg['name']}" for cdir, neg in SHOULD_FAIL_ITEMS],
)
def test_subtle_negative(case_dir: Path, negative: dict) -> None:
    """Subtle mutation — record whether check catches it (never fails test)."""
    case_id = case_dir.name
    ref_code = (case_dir / "reference" / "main.c").read_text(encoding="utf-8")
    bad_code = negative["mutation"](ref_code)

    if bad_code == ref_code:
        pytest.skip(f"Mutation '{negative['name']}' did not change the code")

    all_details = _run_checks_on_code(case_dir, bad_code)

    for check_name in negative["should_fail"]:
        matching = [d for d in all_details if d.check_name == check_name]
        if not matching:
            BLIND_SPOTS.append({
                "case": case_id,
                "mutation": negative["name"],
                "check": check_name,
                "result": "CHECK_NOT_FOUND",
                "bug": negative.get("bug_description", ""),
            })
            continue

        caught = all(not d.passed for d in matching)
        if not caught:
            BLIND_SPOTS.append({
                "case": case_id,
                "mutation": negative["name"],
                "check": check_name,
                "result": "NOT_CAUGHT",
                "bug": negative.get("bug_description", ""),
            })

    # Always passes — this is discovery, not enforcement


def test_subtle_precision_report() -> None:
    """Print the blind spot report after all subtle tests run."""
    # This test runs last (alphabetical order: test_subtle_p... after test_subtle_n...)
    total = len(SHOULD_FAIL_ITEMS)
    caught = total - len(BLIND_SPOTS)

    print(f"\n{'='*60}")
    print(f"CHECK PRECISION REPORT")
    print(f"{'='*60}")
    print(f"Subtle mutations tested: {total}")
    print(f"Caught by checks:        {caught}/{total} ({caught/total*100:.0f}%)" if total else "No subtle tests")
    print(f"Blind spots:             {len(BLIND_SPOTS)}")

    if BLIND_SPOTS:
        print(f"\nBLIND SPOTS (checks that missed bugs):")
        for bs in BLIND_SPOTS:
            print(f"  [{bs['case']}] {bs['mutation']}")
            print(f"    Check: {bs['check']} → {bs['result']}")
            if bs["bug"]:
                print(f"    Bug: {bs['bug']}")
    print(f"{'='*60}")
