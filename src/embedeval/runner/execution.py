"""Single-case execution and the run_benchmark orchestration loop.

call_model and evaluate are called through the package module (``_runner``)
rather than the names imported into this module's globals, so test patches
of ``embedeval.runner.call_model`` / ``embedeval.runner.evaluate`` are seen
at call time. The direct imports remain for the package __init__ re-export
(defining the default, un-patched bindings).
"""

import logging
from pathlib import Path

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from embedeval.corpus import (
    GenerationParams,
    GradeCell,
    corpus_lookup,
    corpus_store,
    grade_lookup,
    grade_store,
    hash_prompt,
)
from embedeval import runner as _runner
from embedeval.llm_client import build_full_prompt
from embedeval.models import (
    CaseMetadata,
    CheckDetail,
    EvalResult,
    LayerResult,
    TokenUsage,
    Visibility,
)

from embedeval.runner.checkpoint import _append_checkpoint, _load_checkpoint
from embedeval.runner.discovery import Filters, discover_cases, filter_cases
from embedeval.runner.prompts import (
    _collect_context_files,
    _inject_board_target,
    _load_prompt,
)

logger = logging.getLogger(__name__)


def _make_error_result(
    meta: CaseMetadata,
    model: str,
    attempt: int,
    exc: BaseException,
) -> EvalResult:
    """Synthesize a FAIL@L0 EvalResult for an unhandled per-case error."""
    error_msg = f"{type(exc).__name__}: {exc}"
    result = EvalResult(
        case_id=meta.id,
        category=meta.category,
        sdk=meta.sdk,
        model=model,
        attempt=attempt,
        generated_code="",
        layers=[
            LayerResult(
                layer=0,
                name="static_analysis",
                passed=False,
                details=[
                    CheckDetail(
                        check_name="llm_call",
                        passed=False,
                        expected="LLM response",
                        actual=error_msg[:500],
                        check_type="llm_error",
                    )
                ],
                error=error_msg[:500],
                duration_seconds=0.0,
                score=0.0,
            )
        ],
        failed_at_layer=0,
        passed=False,
        total_score=0.0,
        duration_seconds=0.0,
        token_usage=TokenUsage(
            input_tokens=0,
            output_tokens=0,
            total_tokens=0,
        ),
        cost_usd=0.0,
    )
    result.tier = meta.tier
    result.reasoning_types = meta.reasoning_types
    return result


def _build_result_from_grade(
    *,
    grade: "GradeCell",
    meta: CaseMetadata,
    model: str,
    attempt: int,
    generated_code: str,
    token_usage: TokenUsage,
    cost_usd: float,
    temperature: float,
    gen_params: dict,
    used_thinking: bool,
    prose_retry: bool = False,
    llm_duration_seconds: float = 0.0,
) -> EvalResult:
    """Reconstruct an EvalResult from a cached GradeCell + current call metadata.

    The GradeCell only stores the check pipeline output (layers, passed,
    failed_at_layer, total_score). Per-call fields like model, attempt,
    token_usage, cost_usd come from the current invocation so a hit never
    leaks state from the call that originally populated the cache.
    llm_duration_seconds is 0.0 for generation cache hits (no LLM call made).
    """
    return EvalResult(
        case_id=meta.id,
        category=meta.category,
        sdk=meta.sdk,
        model=model,
        attempt=attempt,
        generated_code=generated_code,
        layers=grade.layers,
        failed_at_layer=grade.failed_at_layer,
        passed=grade.passed,
        total_score=grade.total_score,
        duration_seconds=llm_duration_seconds,
        token_usage=token_usage,
        cost_usd=cost_usd,
        tier=meta.tier,
        reasoning_types=meta.reasoning_types,
        used_thinking=used_thinking,
        prose_retry=prose_retry,
        temperature=temperature,
        generation_params=gen_params,
    )


def _run_single_case(
    *,
    meta: CaseMetadata,
    case_dir: Path,
    prompt: str,
    context_files: list[str],
    model: str,
    attempt: int,
    feedback_rounds: int,
    context_pack: str | None = None,
    no_think: bool = False,
    corpus_dir: Path | None = None,
    prompt_hash: str | None = None,
    temperature: float = 0.0,
    gen_params_dict: dict | None = None,
    force: bool = False,
) -> EvalResult:
    """Evaluate one case/attempt — extracted so the caller can wrap it
    in a broad try/except without duplicating the happy-path logic.

    When corpus_dir and prompt_hash are provided, checks the generation
    corpus before calling the model.  On a cache hit the stored
    generated_code is used directly (no LLM call).  The result is written
    to the corpus on every cache miss so subsequent runs can reuse it.
    """
    gen_params = gen_params_dict or {}

    # --- corpus lookup (cache hit → skip LLM call) ---
    cached_code: str | None = None
    if corpus_dir is not None and prompt_hash is not None and not force:
        cell = corpus_lookup(
            corpus_dir=corpus_dir,
            case_id=meta.id,
            model=model,
            attempt=attempt,
            prompt_hash=prompt_hash,
            temperature=temperature,
            generation_params=gen_params,
        )
        if cell is not None:
            logger.info(
                "Corpus hit: %s attempt %d — skipping LLM call",
                meta.id,
                attempt,
            )
            cached_code = cell.generated_code

    if cached_code is not None:
        # Generation cache hit — re-grade from cached code.
        # Check grading cache first: if checks haven't changed either, skip evaluate().
        if corpus_dir is not None and not force:
            cached_grade = grade_lookup(corpus_dir, cached_code, case_dir)
            if cached_grade is not None:
                logger.info(
                    "Grade cache hit: %s attempt %d — skipping evaluate()",
                    meta.id,
                    attempt,
                )
                return _build_result_from_grade(
                    grade=cached_grade,
                    meta=meta,
                    model=model,
                    attempt=attempt,
                    generated_code=cached_code,
                    token_usage=TokenUsage(
                        input_tokens=0, output_tokens=0, total_tokens=0
                    ),
                    cost_usd=0.0,
                    temperature=temperature,
                    gen_params=gen_params,
                    used_thinking=False,
                )

        result = _runner.evaluate(
            case_dir=case_dir,
            generated_code=cached_code,
            model=model,
            attempt=attempt,
            token_usage=TokenUsage(input_tokens=0, output_tokens=0, total_tokens=0),
            cost_usd=0.0,
            category=meta.category,
        )
        result.sdk = meta.sdk
        result.tier = meta.tier
        result.reasoning_types = meta.reasoning_types
        result.temperature = temperature
        result.generation_params = gen_params
        if corpus_dir is not None:
            grade_store(corpus_dir, cached_code, case_dir, result)
        return result

    llm_response = _runner.call_model(
        model=model,
        prompt=prompt,
        context_files=context_files,
        context_pack=context_pack,
        no_think=no_think,
    )

    # --- corpus store (generation cache miss → persist after LLM call) ---
    if corpus_dir is not None and prompt_hash is not None:
        corpus_store(
            corpus_dir=corpus_dir,
            case_id=meta.id,
            model=model,
            attempt=attempt,
            prompt_hash=prompt_hash,
            temperature=temperature,
            generation_params=gen_params,
            generated_code=llm_response.generated_code,
            input_tokens=llm_response.token_usage.input_tokens,
            output_tokens=llm_response.token_usage.output_tokens,
            cost_usd=llm_response.cost_usd,
        )

    # --- grading cache lookup (new generation, but checks may be unchanged) ---
    if corpus_dir is not None and not force:
        cached_grade = grade_lookup(
            corpus_dir, llm_response.generated_code, case_dir
        )
        if cached_grade is not None:
            logger.info(
                "Grade cache hit (post-LLM): %s attempt %d — skipping evaluate()",
                meta.id,
                attempt,
            )
            result = _build_result_from_grade(
                grade=cached_grade,
                meta=meta,
                model=model,
                attempt=attempt,
                generated_code=llm_response.generated_code,
                token_usage=llm_response.token_usage,
                cost_usd=llm_response.cost_usd,
                temperature=temperature,
                gen_params=gen_params,
                used_thinking=bool(llm_response.thinking_content),
                prose_retry=llm_response.prose_retry,
                llm_duration_seconds=llm_response.duration_seconds,
            )
            # Skip feedback loop: a cached grade means we already know the
            # outcome; if the user wants to re-run feedback they must --force.
            return result

    result = _runner.evaluate(
        case_dir=case_dir,
        generated_code=llm_response.generated_code,
        model=model,
        attempt=attempt,
        token_usage=llm_response.token_usage,
        cost_usd=llm_response.cost_usd,
        category=meta.category,
    )
    result.sdk = meta.sdk
    result.tier = meta.tier
    result.reasoning_types = meta.reasoning_types
    result.used_thinking = bool(llm_response.thinking_content)
    result.prose_retry = llm_response.prose_retry
    result.temperature = temperature
    result.generation_params = gen_params
    result.duration_seconds = llm_response.duration_seconds
    if corpus_dir is not None:
        grade_store(corpus_dir, llm_response.generated_code, case_dir, result)

    # Compiler feedback loop: retry with error context on early failures.
    # Re-check the failed layer at each iteration: a previous feedback round
    # may have moved the failure deeper (e.g. L0 → L2) or fixed it entirely,
    # in which case feeding back stale L0 errors is wrong.
    feedback_round = 0
    while (
        feedback_round < feedback_rounds
        and not result.passed
        and result.failed_at_layer is not None
        and 0 <= result.failed_at_layer <= 1
        and result.failed_at_layer < len(result.layers)
    ):
        failed_layer = result.layers[result.failed_at_layer]
        error_msg = failed_layer.error or ""
        failed_details = "\n".join(
            f"- {d.check_name}: expected={d.expected}, actual={d.actual}"
            for d in failed_layer.details
            if not d.passed
        )
        error_info = (
            "\n".join(filter(None, [error_msg, failed_details])) or "Check failed"
        )
        feedback_prompt = (
            f"Your previous code had the following error:\n"
            f"```\n{error_info[:800]}\n```\n\n"
            f"Original task:\n{prompt}\n\n"
            f"Please fix the code and output ONLY the complete"
            f" corrected C source file."
        )
        fb_response = _runner.call_model(
            model=model,
            prompt=feedback_prompt,
            context_pack=context_pack,
            no_think=no_think,
        )
        fb_code = fb_response.generated_code

        # NOTE: feedback rounds bypass the grading cache. The cache is keyed
        # on (code_hash, checks_hash) which doesn't distinguish a base
        # generation from a feedback-round output, so storing fb_code grades
        # would poison future base lookups (and vice versa). Feedback rounds
        # always re-evaluate.
        result = _runner.evaluate(
            case_dir=case_dir,
            generated_code=fb_code,
            model=model,
            attempt=attempt,
            token_usage=fb_response.token_usage,
            cost_usd=fb_response.cost_usd,
            category=meta.category,
        )
        result.sdk = meta.sdk
        result.tier = meta.tier
        result.reasoning_types = meta.reasoning_types
        result.temperature = temperature
        result.generation_params = gen_params
        result.duration_seconds = fb_response.duration_seconds

        logger.info(
            "Feedback round %d/%d for case %s: %s",
            feedback_round + 1,
            feedback_rounds,
            meta.id,
            "PASS" if result.passed else f"FAIL@L{result.failed_at_layer}",
        )
        feedback_round += 1
        if result.passed:
            break

    return result


def run_benchmark(
    cases_dir: Path,
    model: str,
    filters: Filters | None = None,
    attempts: int = 1,
    feedback_rounds: int = 0,
    include_private: bool = False,
    extra_cases_dirs: list[Path] | None = None,
    checkpoint_path: Path | None = None,
    context_pack: str | None = None,
    no_think: bool = False,
    corpus_dir: Path | None = None,
    temperature: float = 0.0,
    force: bool = False,
) -> list[EvalResult]:
    """Run the benchmark pipeline: discover, filter, LLM call, evaluate.

    Args:
        cases_dir: Root directory containing case subdirectories.
        model: Model identifier for LLM calls.
        filters: Optional filtering criteria.
        attempts: Number of attempts per case (for pass@k calculation).
        feedback_rounds: Number of compiler-feedback retry rounds (0 = disabled).
            When > 0 and a case fails at L0 or L1, the error message is fed back
            to the LLM for up to `feedback_rounds` additional attempts.
        include_private: If True, include private (held-out) cases.
            Defaults to False for contamination prevention.
        extra_cases_dirs: Additional directories to discover cases from
            (e.g., private cases from a separate repo).
        checkpoint_path: Optional path to a JSONL checkpoint file.
            If the file exists, previously completed cases are loaded
            and skipped. Each newly completed case is appended
            immediately so the run can resume after an interruption.
        context_pack: Optional run-wide context (team CLAUDE.md or expert
            pack content) prepended to every LLM prompt. See
            docs/CONTEXT-QUALITY-MODE.md.
        corpus_dir: Directory for the generation cache.  When provided,
            completed cells are looked up before calling the model, and
            new cells are stored after each LLM call.
        temperature: LLM sampling temperature — stored in each CorpusCell
            so the cache can detect key mismatches on reruns.
        force: When True, bypass the corpus lookup and always call the
            model, overwriting any existing cells in the corpus.

    Returns:
        List of EvalResult for all case/attempt combinations.
    """
    effective_filters = filters or Filters()
    if not include_private and effective_filters.visibility is None:
        effective_filters.visibility = Visibility.PUBLIC
    all_cases = discover_cases(cases_dir)
    for extra_dir in extra_cases_dirs or []:
        all_cases.extend(discover_cases(extra_dir))
    selected = filter_cases(all_cases, effective_filters)

    if not selected:
        logger.warning("No cases selected after filtering")
        return []

    # Load checkpoint from a prior interrupted run (if any)
    completed: dict[str, EvalResult] = {}
    if checkpoint_path is not None:
        completed = _load_checkpoint(checkpoint_path)

    # Build the generation params dict once — same for all cells in this run.
    gen_params_dict = GenerationParams(
        no_think=no_think,
        feedback_rounds=feedback_rounds,
    ).as_sorted_dict()

    results: list[EvalResult] = list(completed.values())
    total_tasks = len(selected) * attempts
    skipped = 0

    # Pre-run cache summary: count how many cells are already in the generation cache
    if corpus_dir is not None:
        gen_params_dict_for_check = GenerationParams(
            no_think=no_think,
            feedback_rounds=feedback_rounds,
        ).as_sorted_dict()
        cache_hits = 0
        cache_misses = 0
        for case_dir, meta in selected:
            if meta.id in completed:
                continue
            prompt = _load_prompt(case_dir)
            prompt = _inject_board_target(prompt, meta)
            context_files = _collect_context_files(case_dir)
            full_prompt_for_hash = build_full_prompt(prompt, context_files, context_pack)
            if no_think:
                full_prompt_for_hash = full_prompt_for_hash + "\n/no_think"
            ph = hash_prompt(full_prompt_for_hash)
            for attempt in range(1, attempts + 1):
                cell = corpus_lookup(
                    corpus_dir=corpus_dir,
                    model=model,
                    case_id=meta.id,
                    prompt_hash=ph,
                    attempt=attempt,
                    temperature=temperature,
                    generation_params=gen_params_dict_for_check,
                )
                if cell is not None:
                    cache_hits += 1
                else:
                    cache_misses += 1
        console = Console()
        total_cells = cache_hits + cache_misses
        console.print(
            f"[bold]Cache:[/bold] {cache_hits}/{total_cells} cells cached "
            f"([green]{cache_hits} hits[/green], [yellow]{cache_misses} LLM calls[/yellow])"
        )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task(
            f"Running {len(selected)} cases x {attempts} attempts",
            total=total_tasks,
        )

        for case_dir, meta in selected:
            # Skip cases already completed in a prior (interrupted) run
            if meta.id in completed:
                skipped += 1
                progress.advance(task, advance=attempts)
                continue

            prompt = _load_prompt(case_dir)
            prompt = _inject_board_target(prompt, meta)
            context_files = _collect_context_files(case_dir)

            # Compute the hash of the full prompt as the model will see it.
            # Must include context_pack and no_think suffix so any change
            # to the prompt composition causes a cache miss.
            full_prompt_for_hash = build_full_prompt(prompt, context_files, context_pack)
            if no_think:
                full_prompt_for_hash = full_prompt_for_hash + "\n/no_think"
            prompt_hash = hash_prompt(full_prompt_for_hash)

            for attempt in range(1, attempts + 1):
                progress.update(
                    task,
                    description=f"[{meta.id}] attempt {attempt}/{attempts}",
                )

                try:
                    result = _run_single_case(
                        meta=meta,
                        case_dir=case_dir,
                        prompt=prompt,
                        context_files=context_files,
                        model=model,
                        attempt=attempt,
                        feedback_rounds=feedback_rounds,
                        context_pack=context_pack,
                        no_think=no_think,
                        corpus_dir=corpus_dir,
                        prompt_hash=prompt_hash,
                        temperature=temperature,
                        gen_params_dict=gen_params_dict,
                        force=force,
                    )
                except Exception as exc:  # noqa: BLE001
                    # Catch ANY per-case error (UnicodeDecodeError,
                    # network timeouts, JSON parse failures, etc.) so
                    # one broken case doesn't kill the entire run.
                    logger.exception(
                        "Case %s attempt %d: unhandled %s — recording FAIL@L0",
                        meta.id,
                        attempt,
                        type(exc).__name__,
                    )
                    result = _make_error_result(meta, model, attempt, exc)

                results.append(result)
                progress.advance(task)

                # Checkpoint: persist immediately so crashes don't
                # discard hours of prior progress.
                if checkpoint_path is not None:
                    _append_checkpoint(checkpoint_path, result)

                status = "PASS" if result.passed else f"FAIL@L{result.failed_at_layer}"
                logger.info(
                    "Case %s attempt %d: %s",
                    meta.id,
                    attempt,
                    status,
                )

    if skipped:
        logger.info(
            "Resumed from checkpoint: %d cases skipped, %d new",
            skipped,
            len(results) - len(completed),
        )
    logger.info("Benchmark complete: %d results", len(results))
    return results
