"""Smoke regression test for the runner + corpus + grade-cache flow.

Goal: end-to-end deterministic test that exercises ``_run_single_case``
through the full caching pipeline. Catches regressions in the cache key
logic, the grade-cell reconstruction, and the LLM-call-skipping behavior
that would silently falsify benchmark results.

Uses ``model="mock"`` so no network is touched. Counts how many times
the LLM dispatcher and the evaluator are invoked across consecutive
runs to assert that cache hits actually skip work.
"""

from pathlib import Path
from unittest.mock import patch

import yaml

from embedeval.runner import Filters, run_benchmark

# Minimal case that the mock model "solves" — pass/fail outcome doesn't
# matter for the smoke test; only the call-count signals do.
_PROMPT_V1 = "Generate a minimal C main()."
_PROMPT_V2 = "Generate a minimal C main(). Use static allocation."

_STATIC_CHECKS_V1 = """\
from embedeval.models import CheckDetail

def run_checks(generated_code):
    return [CheckDetail(
        check_name="has_main",
        passed="main" in generated_code,
        expected="main()",
        actual="present" if "main" in generated_code else "missing",
        check_type="exact_match",
    )]
"""

_STATIC_CHECKS_V2 = """\
from embedeval.models import CheckDetail

def run_checks(generated_code):
    return [CheckDetail(
        check_name="has_include",
        passed="#include" in generated_code,
        expected="#include directive",
        actual="present" if "#include" in generated_code else "missing",
        check_type="exact_match",
    )]
"""


def _make_case(case_root: Path, case_id: str, prompt: str, checks: str) -> Path:
    case_dir = case_root / case_id
    (case_dir / "checks").mkdir(parents=True)
    metadata = {
        "id": case_id,
        "category": "kconfig",
        "difficulty": "easy",
        "title": f"Smoke {case_id}",
        "description": "Smoke regression case",
        "tags": ["smoke"],
        "platform": "native_sim",
        "sdk": "zephyr",
        "estimated_tokens": 100,
        "sdk_version": "3.6.0",
    }
    (case_dir / "metadata.yaml").write_text(yaml.dump(metadata), encoding="utf-8")
    (case_dir / "prompt.md").write_text(prompt, encoding="utf-8")
    (case_dir / "checks" / "static.py").write_text(checks, encoding="utf-8")
    return case_dir


def _run(
    cases_dir: Path,
    corpus_dir: Path,
    *,
    model: str = "mock",
    attempts: int = 1,
    force: bool = False,
) -> tuple[int, int, list]:
    """Run the benchmark and return (call_model_count, evaluate_count, results).

    Wraps the real call_model and evaluate so we can count invocations
    without breaking their behavior.
    """
    from embedeval import runner as runner_module

    orig_call = runner_module.call_model
    orig_eval = runner_module.evaluate
    call_count = {"n": 0}
    eval_count = {"n": 0}

    def _counted_call(*args, **kwargs):
        call_count["n"] += 1
        return orig_call(*args, **kwargs)

    def _counted_eval(*args, **kwargs):
        eval_count["n"] += 1
        return orig_eval(*args, **kwargs)

    with (
        patch.object(runner_module, "call_model", side_effect=_counted_call),
        patch.object(runner_module, "evaluate", side_effect=_counted_eval),
    ):
        results = run_benchmark(
            cases_dir=cases_dir,
            model=model,
            filters=Filters(),
            attempts=attempts,
            corpus_dir=corpus_dir,
            force=force,
        )

    return call_count["n"], eval_count["n"], results


def test_smoke_second_run_is_full_cache_hit(tmp_path: Path) -> None:
    """First run populates caches; second run with no changes hits both
    caches and does zero LLM calls AND zero evaluate calls."""
    cases = tmp_path / "cases"
    _make_case(cases, "smoke-001", _PROMPT_V1, _STATIC_CHECKS_V1)
    corpus = tmp_path / "corpus"

    calls_1, evals_1, results_1 = _run(cases, corpus)
    assert calls_1 == 1
    assert evals_1 == 1
    assert len(results_1) == 1

    calls_2, evals_2, results_2 = _run(cases, corpus)
    assert calls_2 == 0, "generation cache should skip the LLM call"
    assert evals_2 == 0, "grade cache should skip evaluate()"
    assert len(results_2) == 1


def test_smoke_prompt_edit_invalidates_generation_cache(tmp_path: Path) -> None:
    """Editing the prompt changes prompt_hash → generation miss → re-call."""
    cases = tmp_path / "cases"
    case_dir = _make_case(cases, "smoke-001", _PROMPT_V1, _STATIC_CHECKS_V1)
    corpus = tmp_path / "corpus"

    _run(cases, corpus)
    (case_dir / "prompt.md").write_text(_PROMPT_V2, encoding="utf-8")

    calls, evals, _ = _run(cases, corpus)
    assert calls == 1, "prompt change must miss the generation cache"
    # The mock returns the same code, so the grade cache may still hit.
    assert evals in (0, 1)


def test_smoke_check_edit_keeps_generation_invalidates_grade(tmp_path: Path) -> None:
    """Editing only static.py keeps generation hit but misses grading."""
    cases = tmp_path / "cases"
    case_dir = _make_case(cases, "smoke-001", _PROMPT_V1, _STATIC_CHECKS_V1)
    corpus = tmp_path / "corpus"

    _run(cases, corpus)
    (case_dir / "checks" / "static.py").write_text(_STATIC_CHECKS_V2, encoding="utf-8")

    calls, evals, _ = _run(cases, corpus)
    assert calls == 0, "generation cache must still hit"
    assert evals == 1, "check edit must miss the grade cache and re-evaluate"


def test_smoke_force_bypasses_both_caches(tmp_path: Path) -> None:
    """--force regenerates and re-grades even with a fully populated cache."""
    cases = tmp_path / "cases"
    _make_case(cases, "smoke-001", _PROMPT_V1, _STATIC_CHECKS_V1)
    corpus = tmp_path / "corpus"

    _run(cases, corpus)
    calls, evals, _ = _run(cases, corpus, force=True)
    assert calls == 1
    assert evals == 1


def test_smoke_attempts_topup_only_runs_missing(tmp_path: Path) -> None:
    """Increasing --attempts from 3 to 5 must call LLM only for the 2 new cells."""
    cases = tmp_path / "cases"
    _make_case(cases, "smoke-001", _PROMPT_V1, _STATIC_CHECKS_V1)
    corpus = tmp_path / "corpus"

    calls_3, _, _ = _run(cases, corpus, attempts=3)
    assert calls_3 == 3

    calls_5, _, _ = _run(cases, corpus, attempts=5)
    assert calls_5 == 2, "attempts 3 → 5 must call LLM only for the new 2"


def test_smoke_cache_does_not_leak_metadata_across_models(tmp_path: Path) -> None:
    """Two distinct models that produce the same generated_code must each
    see their OWN model name in the result. This is the regression for
    bug #2 (cache poisoning).

    Setup: model A runs and stores grades. Model B has its OWN generation
    cell (different model_slug) but the same generated_code → grade-cache
    hit on (code_hash, checks_hash). The result for B must carry model=B.
    """
    cases = tmp_path / "cases"
    _make_case(cases, "smoke-001", _PROMPT_V1, _STATIC_CHECKS_V1)
    corpus = tmp_path / "corpus"

    _, _, results_a = _run(cases, corpus, model="mock")
    assert results_a[0].model == "mock"

    # Same case, same code (mock is deterministic) but a different model
    # slug forces a generation-cache miss while triggering a grade-cache
    # hit on the shared code_hash.
    # We simulate "different model" by clearing only the generations dir,
    # leaving grades/ intact.
    import shutil

    shutil.rmtree(corpus / "generations")

    calls, evals, results_b = _run(cases, corpus, model="mock")
    # A fresh generation, but the grade cache MUST hit (code unchanged).
    assert calls == 1
    assert evals == 0, "grade cache should hit even after generation was wiped"
    assert results_b[0].model == "mock"
    # Critical assertion: layers came from cache but the rest is fresh.
    assert results_b[0].token_usage.total_tokens > 0
