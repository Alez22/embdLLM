"""Tests for the grading cache (corpus.py grade_lookup / grade_store).

Regression coverage for bug #2: the previous implementation stored the
full EvalResult (with model, attempt, token_usage, cost_usd, ...) keyed
only on (code_hash, checks_hash). A cache hit from a different model
or attempt would leak those fields into the new result. The GradeCell
fix stores only the check pipeline output; per-call metadata must come
from the caller.
"""

from pathlib import Path

from embedeval.corpus import GradeCell, grade_lookup, grade_store
from embedeval.models import (
    CaseCategory,
    CaseMetadata,
    CaseTier,
    CheckDetail,
    EvalResult,
    LayerResult,
    Sdk,
    TokenUsage,
    Visibility,
)
from embedeval.runner import _build_result_from_grade


def _make_eval_result(
    *,
    model: str,
    attempt: int,
    input_tokens: int,
    cost: float,
    passed: bool = True,
) -> EvalResult:
    return EvalResult(
        case_id="case-001",
        category=CaseCategory.KCONFIG,
        sdk=Sdk.ZEPHYR,
        model=model,
        attempt=attempt,
        generated_code="int main(){}",
        layers=[
            LayerResult(
                layer=0,
                name="static_analysis",
                passed=passed,
                details=[
                    CheckDetail(
                        check_name="hdr",
                        passed=passed,
                        expected="x",
                        actual="x" if passed else "missing",
                        check_type="exact_match",
                    )
                ],
                duration_seconds=0.0,
            )
        ],
        failed_at_layer=None if passed else 0,
        passed=passed,
        total_score=1.0 if passed else 0.0,
        duration_seconds=12.34,
        token_usage=TokenUsage(
            input_tokens=input_tokens,
            output_tokens=20,
            total_tokens=input_tokens + 20,
        ),
        cost_usd=cost,
    )


def _make_case_meta() -> CaseMetadata:
    return CaseMetadata(
        id="case-001",
        category=CaseCategory.KCONFIG,
        difficulty="easy",
        title="Test",
        description="d",
        tags=["t"],
        platform="native_sim",
        sdk=Sdk.ZEPHYR,
        sdk_version="3.6.0",
        estimated_tokens=100,
        visibility=Visibility.PUBLIC,
        tier=CaseTier.CORE,
    )


def _make_case_dir(tmp_path: Path) -> Path:
    case_dir = tmp_path / "case-001"
    (case_dir / "checks").mkdir(parents=True)
    (case_dir / "checks" / "static.py").write_text("# check\n")
    return case_dir


def test_grade_cell_excludes_per_call_fields(tmp_path: Path) -> None:
    """Cached cell must NOT carry model, attempt, token_usage, cost_usd."""
    case_dir = _make_case_dir(tmp_path)
    corpus_dir = tmp_path / "corpus"

    original = _make_eval_result(
        model="groq/llama-3.3-70b", attempt=1, input_tokens=500, cost=0.001
    )
    grade_store(corpus_dir, "code-a", case_dir, original)

    cached = grade_lookup(corpus_dir, "code-a", case_dir)
    assert isinstance(cached, GradeCell)
    # GradeCell exposes only the check pipeline output.
    assert hasattr(cached, "layers")
    assert hasattr(cached, "passed")
    assert hasattr(cached, "failed_at_layer")
    assert hasattr(cached, "total_score")
    # Crucially: no per-call leakage.
    assert not hasattr(cached, "model")
    assert not hasattr(cached, "attempt")
    assert not hasattr(cached, "token_usage")
    assert not hasattr(cached, "cost_usd")


def test_grade_cache_does_not_leak_model_across_lookups(tmp_path: Path) -> None:
    """Two distinct models reading the same cached code must each see THEIR
    OWN model name in the reconstructed EvalResult, not the originator's."""
    case_dir = _make_case_dir(tmp_path)
    corpus_dir = tmp_path / "corpus"

    original = _make_eval_result(
        model="model-A", attempt=1, input_tokens=500, cost=0.005
    )
    grade_store(corpus_dir, "shared-code", case_dir, original)

    cell = grade_lookup(corpus_dir, "shared-code", case_dir)
    assert cell is not None

    # Model B reads the same cache entry.
    result_b = _build_result_from_grade(
        grade=cell,
        meta=_make_case_meta(),
        model="model-B",
        attempt=3,
        generated_code="shared-code",
        token_usage=TokenUsage(input_tokens=999, output_tokens=11, total_tokens=1010),
        cost_usd=0.099,
        temperature=0.7,
        gen_params={"feedback_rounds": 0, "no_think": False},
        used_thinking=True,
    )

    # Per-call fields come from the lookup site, NOT from the originator.
    assert result_b.model == "model-B"
    assert result_b.attempt == 3
    assert result_b.token_usage.input_tokens == 999
    assert result_b.cost_usd == 0.099
    assert result_b.temperature == 0.7
    assert result_b.used_thinking is True

    # Check pipeline fields come from the cache.
    assert result_b.passed is True
    assert result_b.failed_at_layer is None
    assert len(result_b.layers) == 1
    assert result_b.layers[0].details[0].check_name == "hdr"


def test_grade_cache_miss_on_different_checks(tmp_path: Path) -> None:
    """Editing checks invalidates the cache."""
    case_dir = _make_case_dir(tmp_path)
    corpus_dir = tmp_path / "corpus"

    original = _make_eval_result(
        model="m", attempt=1, input_tokens=100, cost=0.0
    )
    grade_store(corpus_dir, "code-x", case_dir, original)

    # Modify the check file → checks_hash changes → cache miss.
    (case_dir / "checks" / "static.py").write_text("# different check\n")
    assert grade_lookup(corpus_dir, "code-x", case_dir) is None


def test_grade_cache_miss_on_different_code(tmp_path: Path) -> None:
    """Different generated_code → different code_hash → cache miss."""
    case_dir = _make_case_dir(tmp_path)
    corpus_dir = tmp_path / "corpus"

    original = _make_eval_result(
        model="m", attempt=1, input_tokens=100, cost=0.0
    )
    grade_store(corpus_dir, "code-1", case_dir, original)
    assert grade_lookup(corpus_dir, "code-2", case_dir) is None
