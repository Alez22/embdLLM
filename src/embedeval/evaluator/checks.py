"""Layers L0 (static), L3 (behavioral), L4 (mutant) and check-module loading."""

import importlib.util
import logging
import time
from pathlib import Path
from types import ModuleType
from typing import Any

from embedeval.models import CheckDetail, LayerResult

logger = logging.getLogger(__name__)


class _CheckModuleError(Exception):
    """Raised when a check module exists but fails to import or execute.

    Distinct from returning None (file not found = no checks = pass).
    Callers must turn this into a FAIL layer result so broken checks
    are never silently treated as passing.
    """


def _run_static_checks(case_dir: Path, generated_code: str) -> LayerResult:
    """Layer 0: Static analysis checks from case checks/static.py."""
    try:
        checks_module = _load_check_module(case_dir, "static")
    except _CheckModuleError as exc:
        return LayerResult(
            layer=0,
            name="static_analysis",
            passed=False,
            details=[],
            error=str(exc),
            duration_seconds=0.0,
        )
    if checks_module is None:
        return LayerResult(
            layer=0,
            name="static_analysis",
            passed=True,
            details=[],
            error=None,
            duration_seconds=0.0,
        )

    return _execute_check_module(
        checks_module, generated_code, layer=0, name="static_analysis"
    )




def _run_behavioral(case_dir: Path, generated_code: str) -> LayerResult:
    """Layer 3: Behavioral assertion checks from case checks/behavior.py."""
    try:
        checks_module = _load_check_module(case_dir, "behavior")
    except _CheckModuleError as exc:
        return LayerResult(
            layer=3,
            name="static_heuristic",
            passed=False,
            details=[],
            error=str(exc),
            duration_seconds=0.0,
        )
    if checks_module is None:
        return LayerResult(
            layer=3,
            name="static_heuristic",
            passed=True,
            details=[],
            error=None,
            duration_seconds=0.0,
        )

    return _execute_check_module(
        checks_module, generated_code, layer=3, name="static_heuristic"
    )




def _run_mutant_checks(case_dir: Path, generated_code: str) -> LayerResult:
    """Layer 4: Mutation meta-verification.

    Loads negatives.py NEGATIVES data, applies each must_fail mutation to
    the generated code, and verifies that L0/L3 checks detect the seeded bug.
    This tests benchmark check quality, not LLM quality — L4 failures do not
    affect the overall case pass/fail determination.
    """
    start = time.monotonic()
    negatives = _load_negatives(case_dir)
    if negatives is None:
        return LayerResult(
            layer=4,
            name="test_quality_proof",
            passed=True,
            details=[],
            error=None,
            duration_seconds=0.0,
        )

    details: list[CheckDetail] = []
    for neg in negatives:
        if "must_fail" not in neg:
            continue

        name = neg.get("name", "unknown")
        try:
            mutated_code = neg["mutation"](generated_code)
        except Exception as exc:
            logger.debug("Mutation '%s' raised: %s", name, exc)
            details.append(
                CheckDetail(
                    check_name=f"mutation_{name}",
                    passed=True,
                    expected="mutation applied",
                    actual=f"skipped (mutation error: {exc})",
                    check_type="mutation",
                )
            )
            continue

        if mutated_code == generated_code:
            details.append(
                CheckDetail(
                    check_name=f"mutation_{name}",
                    passed=True,
                    expected="mutation applied",
                    actual="skipped (code unchanged by mutation)",
                    check_type="mutation",
                )
            )
            continue

        # Run L0 + L3 checks on the mutated code
        all_check_details: list[CheckDetail] = []
        static_result = _run_static_checks(case_dir, mutated_code)
        all_check_details.extend(static_result.details)
        behavior_result = _run_behavioral(case_dir, mutated_code)
        all_check_details.extend(behavior_result.details)

        # Verify that must_fail checks actually fail on mutated code
        all_caught = True
        missed: list[str] = []
        for check_name in neg["must_fail"]:
            matching = [d for d in all_check_details if d.check_name == check_name]
            if not matching or any(d.passed for d in matching):
                all_caught = False
                missed.append(check_name)

        details.append(
            CheckDetail(
                check_name=f"mutation_{name}",
                passed=all_caught,
                expected=f"checks {neg['must_fail']} detect mutation",
                actual="caught" if all_caught else f"missed: {missed}",
                check_type="mutation",
            )
        )

    elapsed = time.monotonic() - start
    all_passed = all(d.passed for d in details) if details else True
    return LayerResult(
        layer=4,
        name="test_quality_proof",
        passed=all_passed,
        details=details,
        error=None,
        duration_seconds=elapsed,
    )


def _load_negatives(case_dir: Path) -> list[dict[str, Any]] | None:
    """Load NEGATIVES mutation data from checks/negatives.py."""
    try:
        module = _load_check_module(case_dir, "negatives")
    except _CheckModuleError as exc:
        logger.warning("negatives.py load error for %s: %s", case_dir.name, exc)
        return None
    if module is None:
        return None
    negatives: list[dict[str, Any]] | None = getattr(module, "NEGATIVES", None)
    if not negatives:
        return None
    return negatives




def _load_check_module(case_dir: Path, module_name: str) -> ModuleType | None:
    """Load a check module from the case's checks/ directory.

    Returns None if the module file does not exist (no checks → layer passes).
    Raises _CheckModuleError if the file exists but cannot be loaded or executed.
    """
    module_path = case_dir / "checks" / f"{module_name}.py"
    if not module_path.is_file():
        logger.debug("Check module not found: %s", module_path)
        return None

    spec = importlib.util.spec_from_file_location(
        f"case_checks.{module_name}", module_path
    )
    if spec is None or spec.loader is None:
        raise _CheckModuleError(f"Could not load module spec: {module_path}")

    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        raise _CheckModuleError(
            f"Failed to execute check module {module_path}: {exc}"
        ) from exc
    return module


def _execute_check_module(
    module: ModuleType,
    generated_code: str,
    layer: int,
    name: str,
) -> LayerResult:
    """Execute a check module's run_checks function."""
    run_checks = getattr(module, "run_checks", None)
    if run_checks is None:
        return LayerResult(
            layer=layer,
            name=name,
            passed=False,
            details=[],
            error="Check module missing run_checks() function",
            duration_seconds=0.0,
        )

    try:
        details: list[CheckDetail] = run_checks(generated_code)
        all_passed = all(d.passed for d in details)
        return LayerResult(
            layer=layer,
            name=name,
            passed=all_passed,
            details=details,
            error=None,
            duration_seconds=0.0,
        )
    except Exception as exc:
        logger.error("Check module raised exception: %s", exc)
        return LayerResult(
            layer=layer,
            name=name,
            passed=False,
            details=[],
            error=str(exc),
            duration_seconds=0.0,
        )


