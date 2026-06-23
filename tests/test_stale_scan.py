"""Tests for the dashboard staleness scan.

Verifies that _scan_stale_cells and _scan_stale_runs correctly flag corpus
cells and past runs whose prompt.md or checks/ changed after they were
produced, by reconstructing the same full-prompt hash the runner uses.
"""

from pathlib import Path

import pytest

import embedeval.dashboard as dash
from embedeval.corpus import corpus_store, hash_checks, hash_code, hash_prompt
from embedeval.llm_client import build_full_prompt


@pytest.fixture(autouse=True)
def _clear_hash_caches():
    """The per-case hash helpers are lru_cached; clear between tests."""
    dash._current_prompt_hash.cache_clear()
    dash._current_checks_hash.cache_clear()
    yield
    dash._current_prompt_hash.cache_clear()
    dash._current_checks_hash.cache_clear()


def _write_case(case_dir: Path, prompt: str, static_check: str) -> None:
    """Create a minimal case with a prompt and one static check file."""
    case_dir.mkdir(parents=True)
    (case_dir / "prompt.md").write_text(prompt, encoding="utf-8")
    (case_dir / "metadata.yaml").write_text("id: c1\n", encoding="utf-8")
    checks = case_dir / "checks"
    checks.mkdir()
    (checks / "static.py").write_text(static_check, encoding="utf-8")


def _current_prompt_hash(case_dir: Path) -> str:
    """Replicate the runner's full-prompt hash for the default run config."""
    prompt = (case_dir / "prompt.md").read_text()
    prompt = prompt.rstrip() + "\n\nTarget board: native_sim\n"
    return hash_prompt(build_full_prompt(prompt, [], None))


def test_scan_flags_prompt_and_checks_changes(tmp_path, monkeypatch):
    cases = tmp_path / "cases" / "bucket"
    case_dir = cases / "c1"
    _write_case(case_dir, "Original prompt.", "CHECK = 1\n")

    corpus = tmp_path / "results" / "corpus"
    code = "int main(void){return 0;}"

    # Store a cell whose prompt_hash matches the case as it is now.
    corpus_store(
        corpus_dir=corpus,
        case_id="c1",
        model="m",
        attempt=1,
        prompt_hash=_current_prompt_hash(case_dir),
        temperature=0.0,
        generation_params={},
        generated_code=code,
        input_tokens=0,
        output_tokens=0,
        cost_usd=0.0,
    )

    monkeypatch.setattr(dash, "RESULTS_DIR", tmp_path / "results")
    monkeypatch.setattr(dash, "CASES_DIR", tmp_path / "cases")

    rows = dash._scan_stale_cells()
    assert len(rows) == 1
    row = rows[0]
    # Prompt aligned, but no grade entry exists yet -> checks-stale.
    assert row["prompt_state"] == "aligned"
    assert row["checks_state"] == "stale"

    # Create the matching grade entry -> checks become aligned.
    grade_dir = corpus / "grades" / hash_code(code)
    grade_dir.mkdir(parents=True)
    (grade_dir / f"{hash_checks(case_dir)}.json").write_text("{}", encoding="utf-8")
    rows = dash._scan_stale_cells()
    assert rows[0]["checks_state"] == "aligned"

    # Edit the prompt -> the cell becomes prompt-stale. The per-case hash is
    # lru_cached (prompts are assumed stable while the dashboard runs), so a
    # mid-process edit requires clearing the cache to be picked up.
    (case_dir / "prompt.md").write_text("Edited prompt.", encoding="utf-8")
    dash._current_prompt_hash.cache_clear()
    rows = dash._scan_stale_cells()
    assert rows[0]["prompt_state"] == "stale"


def test_scan_flags_orphan_case(tmp_path, monkeypatch):
    (tmp_path / "cases").mkdir(parents=True)
    corpus = tmp_path / "results" / "corpus"
    corpus_store(
        corpus_dir=corpus,
        case_id="ghost",
        model="m",
        attempt=1,
        prompt_hash="deadbeef",
        temperature=0.0,
        generation_params={},
        generated_code="x",
        input_tokens=0,
        output_tokens=0,
        cost_usd=0.0,
    )
    monkeypatch.setattr(dash, "RESULTS_DIR", tmp_path / "results")
    monkeypatch.setattr(dash, "CASES_DIR", tmp_path / "cases")

    rows = dash._scan_stale_cells()
    assert len(rows) == 1
    assert rows[0]["orphan"] is True
    assert rows[0]["prompt_state"] == "orphan"


def test_aggregate_by_case_groups_models(tmp_path, monkeypatch):
    cases = tmp_path / "cases" / "bucket"
    case_dir = cases / "c1"
    _write_case(case_dir, "Original prompt.", "CHECK = 1\n")
    monkeypatch.setattr(dash, "RESULTS_DIR", tmp_path / "results")
    monkeypatch.setattr(dash, "CASES_DIR", tmp_path / "cases")

    cur_prompt = _current_prompt_hash(case_dir)

    rows = [
        # model A: prompt aligned, one attempt checks-stale
        {"case_id": "c1", "model": "A", "attempt": 1, "orphan": False,
         "prompt_state": "aligned", "stored_prompt": cur_prompt,
         "current_prompt": cur_prompt, "checks_state": "stale", "current_checks": "x"},
        {"case_id": "c1", "model": "A", "attempt": 2, "orphan": False,
         "prompt_state": "aligned", "stored_prompt": cur_prompt,
         "current_prompt": cur_prompt, "checks_state": "aligned", "current_checks": "x"},
        # model B: prompt stale
        {"case_id": "c1", "model": "B", "attempt": 1, "orphan": False,
         "prompt_state": "stale", "stored_prompt": "old",
         "current_prompt": cur_prompt, "checks_state": "aligned", "current_checks": "x"},
    ]
    out = dash._aggregate_stale_by_case(rows)
    assert len(out) == 1
    case = out[0]
    assert case["case_id"] == "c1"
    assert case["any_stale"] is True
    models = {m["model"]: m for m in case["models"]}
    # A: two attempts, one checks-stale -> aggregated checks-stale
    assert models["A"]["n_attempts"] == 2
    assert models["A"]["checks_state"] == "stale"
    assert models["A"]["prompt_state"] == "aligned"
    # B: prompt-stale
    assert models["B"]["prompt_state"] == "stale"
