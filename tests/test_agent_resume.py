"""Tests for agent resume: continuing a run from turn N+1 and the
agent_run.json archive round-trip."""

from pathlib import Path
from unittest.mock import patch

from embedeval.agent import AgentResult, evaluate_agent
from embedeval.agent_report import (
    build_run_dir,
    load_agent_run,
    write_agent_run,
)
from embedeval.models import (
    CaseCategory,
    CheckDetail,
    EvalResult,
    LayerResult,
    LLMResponse,
    TokenUsage,
)


def _stub_response() -> LLMResponse:
    return LLMResponse(
        model="mock",
        generated_code="int main(void) { return 0; }",
        token_usage=TokenUsage(input_tokens=1, output_tokens=1, total_tokens=2),
        cost_usd=0.01,
        duration_seconds=0.0,
    )


def _eval_result(case_id: str, attempt: int, *, passed: bool) -> EvalResult:
    """Build a minimal EvalResult, failing at L0 when not passed so the
    resume helper has an error layer to reconstruct context from."""
    layer = LayerResult(
        layer=0,
        name="static_analysis",
        passed=passed,
        details=[]
        if passed
        else [
            CheckDetail(
                check_name="header_included",
                passed=False,
                expected="fsl_i2c.h",
                actual="missing",
                check_type="exact_match",
            )
        ],
        error=None if passed else "missing header",
        duration_seconds=0.0,
    )
    return EvalResult(
        case_id=case_id,
        category=CaseCategory.ISR_CONCURRENCY,
        model="mock",
        attempt=attempt,
        generated_code="int main(void) { return 0; }",
        layers=[layer],
        failed_at_layer=None if passed else 0,
        passed=passed,
        total_score=1.0 if passed else 0.0,
        duration_seconds=0.0,
        token_usage=TokenUsage(input_tokens=1, output_tokens=1, total_tokens=2),
        cost_usd=0.01,
    )


def test_evaluate_agent_resumes_from_start_turn(tmp_path: Path) -> None:
    """Resuming with start_turn=3 must run only turn 3 (one LLM call) and
    keep the prior history, with turn numbers staying absolute."""
    case_dir = tmp_path / "fake-case-001"
    case_dir.mkdir()

    prior_history = [
        _eval_result("fake-case-001", 1, passed=False),
        _eval_result("fake-case-001", 2, passed=False),
    ]

    with patch("embedeval.agent.call_model") as mock_call:
        mock_call.return_value = _stub_response()
        with patch("embedeval.agent.evaluate") as mock_eval:
            mock_eval.return_value = _eval_result(
                "fake-case-001", 3, passed=True
            )

            result = evaluate_agent(
                case_dir=case_dir,
                model="mock",
                prompt="task body",
                max_turns=3,
                start_turn=3,
                initial_context=["Turn 1 failed", "Turn 2 failed"],
                prior_history=prior_history,
            )

    # Only turn 3 executed → exactly one LLM call.
    mock_call.assert_called_once()
    # Prior history preserved + the new turn appended.
    assert [r.attempt for r in result.history] == [1, 2, 3]
    assert result.passed
    assert result.turns_used == 3


def test_agent_run_archive_round_trip(tmp_path: Path) -> None:
    """write_agent_run then load_agent_run must preserve pass/turns and the
    full per-turn history, and compute recovery_rate correctly."""
    results = [
        # Passed on turn 1 → not part of the recovery denominator.
        AgentResult(
            case_id="c1",
            passed=True,
            turns_used=1,
            max_turns=3,
            history=[_eval_result("c1", 1, passed=True)],
        ),
        # Failed turn 1, recovered on turn 2.
        AgentResult(
            case_id="c2",
            passed=True,
            turns_used=2,
            max_turns=3,
            history=[
                _eval_result("c2", 1, passed=False),
                _eval_result("c2", 2, passed=True),
            ],
        ),
        # Failed all turns.
        AgentResult(
            case_id="c3",
            passed=False,
            turns_used=3,
            max_turns=3,
            history=[
                _eval_result("c3", t, passed=False) for t in (1, 2, 3)
            ],
        ),
    ]

    run_dir = build_run_dir(tmp_path, "qwen/qwen3", 3)
    write_agent_run(
        run_dir=run_dir,
        model="qwen/qwen3",
        max_turns=3,
        temperature=0.5,
        results=results,
        resumed_from=None,
    )

    loaded = load_agent_run(run_dir)
    assert loaded.model == "qwen/qwen3"
    assert {r.case_id for r in loaded.results} == {"c1", "c2", "c3"}
    c3 = next(r for r in loaded.results if r.case_id == "c3")
    assert [r.attempt for r in c3.history] == [1, 2, 3]

    # recovery_rate: of 2 cases failing turn 1 (c2, c3), 1 recovered (c2).
    import json

    summary = json.loads(
        (run_dir / "agent_run.json").read_text(encoding="utf-8")
    )["summary"]
    assert summary["recovery_rate"] == 0.5
    assert summary["passed_at_turn_hist"] == {"1": 1, "2": 1}
