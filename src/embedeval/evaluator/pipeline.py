"""The 5-layer evaluation pipeline: evaluate(), layer dispatch and scoring.

_get_build_mode is reached through the facade package (``_ev``) so test
patches of ``embedeval.evaluator._get_build_mode`` take effect.
"""

import logging
import shutil
import time
from pathlib import Path

from embedeval import evaluator as _ev
from embedeval.evaluator.build import (
    _prepare_build_dir,
    _run_compile_gate,
    _run_runtime,
)
from embedeval.evaluator.checks import (
    _run_behavioral,
    _run_mutant_checks,
    _run_static_checks,
)
from embedeval.evaluator.support import (
    _is_esp_idf_case,
    _is_l1_skipped,
    _is_stm32_case,
)
from embedeval.models import (
    CaseCategory,
    CheckDetail,
    EvalResult,
    LayerResult,
    TokenUsage,
)

logger = logging.getLogger(__name__)

LAYER_NAMES: dict[int, str] = {
    0: "static_analysis",
    1: "compile_gate",
    2: "runtime_execution",
    3: "static_heuristic",
    4: "test_quality_proof",
}

DEFAULT_TIMEOUT = 300.0


def evaluate(
    case_dir: Path,
    generated_code: str,
    model: str = "unknown",
    attempt: int = 1,
    timeout: float = DEFAULT_TIMEOUT,
    token_usage: TokenUsage | None = None,
    cost_usd: float = 0.0,
    category: "CaseCategory | None" = None,
) -> EvalResult:
    """Run the 5-layer evaluation pipeline on generated code.

    Args:
        case_dir: Path to the case directory containing checks/.
        generated_code: The LLM-generated code to evaluate.
        model: Model identifier for result tracking.
        attempt: Attempt number for this evaluation.
        timeout: Timeout in seconds for subprocess calls.
        token_usage: Token usage from the LLM call.
        cost_usd: Cost of the LLM call.

    Returns:
        EvalResult with per-layer pass/fail results.
    """
    start = time.monotonic()
    effective_token_usage = token_usage or TokenUsage(
        input_tokens=0, output_tokens=0, total_tokens=0
    )

    # Fast-path: model returned no code at all (prose response, extraction failure).
    # Record a dedicated check so the cause is visible in results and dashboard.
    if not generated_code.strip():
        logger.warning("evaluate: empty generated_code for %s attempt %d", case_dir.name, attempt)
        no_code_layer = LayerResult(
            layer=0,
            name="static_analysis",
            passed=False,
            details=[CheckDetail(
                check_name="code_extracted",
                passed=False,
                expected="LLM output contains a C source file",
                actual="empty — model returned prose or no code",
                check_type="constraint",
            )],
            error=None,
            duration_seconds=time.monotonic() - start,
            score=0.0,
        )
        skipped = [
            LayerResult(
                layer=i,
                name=LAYER_NAMES[i],
                passed=False,
                details=[],
                error="Skipped: layer 0 failed (no code extracted)",
                duration_seconds=0.0,
            )
            for i in range(1, 5)
        ]
        return EvalResult(
            case_id=case_dir.name,
            category=category,
            model=model,
            attempt=attempt,
            generated_code="",
            layers=[no_code_layer] + skipped,
            failed_at_layer=0,
            passed=False,
            total_score=0.0,
            token_usage=effective_token_usage,
            cost_usd=cost_usd,
            duration_seconds=time.monotonic() - start,
        )

    layers: list[LayerResult] = []
    failed_at_layer: int | None = None

    # Shared build directory: created once, used by L1 (compile) and L2 (runtime),
    # cleaned up after all layers complete.
    build_dir: Path | None = None
    if (
        _ev._get_build_mode() != "skip"
        and (case_dir / "CMakeLists.txt").is_file()
        and not _is_l1_skipped(case_dir)
    ):
        build_dir = _prepare_build_dir(case_dir, generated_code)

    try:
        for layer_num in range(5):
            layer_name = LAYER_NAMES[layer_num]

            if failed_at_layer is not None:
                logger.info(
                    "Skipping layer %d (%s) due to failure at layer %d",
                    layer_num,
                    layer_name,
                    failed_at_layer,
                )
                layers.append(
                    LayerResult(
                        layer=layer_num,
                        name=layer_name,
                        passed=False,
                        details=[],
                        error=f"Skipped: layer {failed_at_layer} failed",
                        duration_seconds=0.0,
                        score=0.0,
                    )
                )
                continue

            layer_start = time.monotonic()
            layer_result = _run_layer(
                layer_num=layer_num,
                layer_name=layer_name,
                case_dir=case_dir,
                generated_code=generated_code,
                timeout=timeout,
                build_dir=build_dir,
            )
            # Calculate weighted score for the layer
            details = layer_result.details
            total_weight = sum(d.weight for d in details)
            earned_weight = sum(d.weight for d in details if d.passed)
            layer_score = earned_weight / total_weight if total_weight > 0 else 1.0

            layer_result = LayerResult(
                layer=layer_num,
                name=layer_name,
                passed=layer_result.passed,
                details=details,
                error=layer_result.error,
                duration_seconds=time.monotonic() - layer_start,
                score=layer_score,
            )
            layers.append(layer_result)

            if not layer_result.passed and layer_num < 4:
                # L4 (mutation meta-verification) failures don't cascade or
                # affect overall pass/fail — they test benchmark quality, not
                # LLM quality.
                failed_at_layer = layer_num
                logger.info("Layer %d (%s) failed", layer_num, layer_name)

    finally:
        if build_dir is not None:
            shutil.rmtree(build_dir, ignore_errors=True)

    elapsed = time.monotonic() - start
    all_passed = failed_at_layer is None

    # Total score: average over all layers that exist for this case (have check
    # files). Skipped layers contribute 0 so a run that fails at L0 scores lower
    # than one that passes L0 and reaches L3, making attempts comparable.
    scorable_count = _count_scorable_layers(case_dir)
    if scorable_count > 0:
        scored_layers = [ly for ly in layers if ly.layer != 4]
        total_score = sum(
            ly.score for ly in scored_layers
            if _layer_exists_for_case(ly.layer, case_dir)
        ) / scorable_count
    else:
        executed_layers = [ly for ly in layers if ly.details and ly.layer != 4]
        total_score = (
            sum(ly.score for ly in executed_layers) / len(executed_layers)
            if executed_layers
            else 1.0
        )

    return EvalResult(
        case_id=case_dir.name,
        category=category,
        model=model,
        attempt=attempt,
        generated_code=generated_code,
        layers=layers,
        failed_at_layer=failed_at_layer,
        passed=all_passed,
        total_score=total_score,
        duration_seconds=elapsed,
        token_usage=effective_token_usage,
        cost_usd=cost_usd,
    )




def _run_layer(
    layer_num: int,
    layer_name: str,
    case_dir: Path,
    generated_code: str,
    timeout: float,
    build_dir: Path | None = None,
) -> LayerResult:
    """Execute a single evaluation layer."""
    if layer_num == 0:
        return _run_static_checks(case_dir, generated_code)
    elif layer_num == 1:
        return _run_compile_gate(case_dir, generated_code, timeout, build_dir)
    elif layer_num == 2:
        is_esp = _is_esp_idf_case(case_dir)
        is_stm32 = _is_stm32_case(case_dir)
        if is_esp or is_stm32:
            platform = "ESP-IDF" if is_esp else "STM32"
            return LayerResult(
                layer=2,
                name="runtime_execution",
                passed=True,
                details=[
                    CheckDetail(
                        check_name="runtime_skip",
                        passed=True,
                        expected="runtime execution",
                        actual=f"skipped ({platform} QEMU not configured)",
                        check_type="environment",
                    )
                ],
                error=None,
                duration_seconds=0.0,
            )
        return _run_runtime(case_dir, generated_code, timeout, build_dir)
    elif layer_num == 3:
        return _run_behavioral(case_dir, generated_code)
    elif layer_num == 4:
        return _run_mutant_checks(case_dir, generated_code)
    else:
        return LayerResult(
            layer=layer_num,
            name=layer_name,
            passed=False,
            details=[],
            error=f"Unknown layer: {layer_num}",
            duration_seconds=0.0,
        )




def _layer_exists_for_case(layer_num: int, case_dir: Path) -> bool:
    """Return True if the given layer has checks defined for this case."""
    if layer_num == 0:
        return (case_dir / "checks" / "static.py").is_file()
    if layer_num == 1:
        return (case_dir / "CMakeLists.txt").is_file() and not _is_l1_skipped(case_dir)
    if layer_num == 2:
        # L2 runtime only exists when L1 exists and is not environment-skipped
        return (case_dir / "CMakeLists.txt").is_file() and not _is_l1_skipped(case_dir)
    if layer_num == 3:
        return (case_dir / "checks" / "behavior.py").is_file()
    return False  # L4 excluded from scoring


def _count_scorable_layers(case_dir: Path) -> int:
    """Return how many layers have checks defined for this case (L4 excluded)."""
    return sum(1 for ln in range(4) if _layer_exists_for_case(ln, case_dir))


