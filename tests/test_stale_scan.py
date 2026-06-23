"""Tests for the dashboard staleness scan.

Verifies that _scan_stale_cells correctly flags corpus generation cells whose
prompt.md or checks/ changed after the cell was produced, by reconstructing the
same full-prompt hash the runner uses.
"""

from pathlib import Path

import embedeval.dashboard as dash
from embedeval.corpus import corpus_store, hash_checks, hash_code, hash_prompt
from embedeval.llm_client import build_full_prompt


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

    # Edit the prompt -> the cell becomes prompt-stale.
    (case_dir / "prompt.md").write_text("Edited prompt.", encoding="utf-8")
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
