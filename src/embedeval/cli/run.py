"""The `run` command: execute a benchmark across cases/models."""

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Optional

import typer

from embedeval.cli.app import _parse_sdk_filter, app
from embedeval.models import CaseCategory, DifficultyTier, EvalResult, Visibility

if TYPE_CHECKING:
    from embedeval.models import CaseMetadata
    from embedeval.result_tracker import TrackerData

logger = logging.getLogger(__name__)

# Matches LAYER_ORDER in reporter.py — kept here to synthesize per-layer
# result fields when rebuilding EvalResults from tracker entries.
_LAYER_NAMES: list[str] = [
    "static_analysis",
    "compile_gate",
    "runtime_execution",
    "static_heuristic",
    "test_quality_proof",
]


def _build_comprehensive_results(
    new_results: list["EvalResult"],
    tracker: "TrackerData",
    model: str,
    all_cases_meta: dict[str, "CaseMetadata"],
) -> list["EvalResult"]:
    """Merge the current run's EvalResults with prior tracker state.

    Leaderboard/run-archive consumers expect a *comprehensive* per-model
    snapshot, not just the cases that happened to be retested this run.
    For every case in the tracker that isn't in `new_results`, this
    synthesizes a minimal EvalResult from the stored pass/failed_layer
    plus CaseMetadata (category/tier/reasoning types). New results take
    priority when a case_id overlaps.

    Cases with orphaned tracker entries (no matching CaseMetadata,
    e.g. deleted TCs) are skipped to avoid polluting aggregates.
    """
    from embedeval.models import EvalResult, LayerResult, TokenUsage

    new_ids = {r.case_id for r in new_results}
    merged: list[EvalResult] = list(new_results)

    prior = tracker.results.get(model, {})
    for case_id, cr in prior.items():
        if case_id in new_ids:
            continue
        meta = all_cases_meta.get(case_id)
        if meta is None:
            continue

        failed_layer = cr.failed_at_layer
        layers: list[LayerResult] = []
        for idx, name in enumerate(_LAYER_NAMES):
            if cr.passed:
                layer_passed = True
                layer_error: str | None = None
            elif failed_layer is None:
                layer_passed = False
                layer_error = None
            elif idx < failed_layer:
                layer_passed = True
                layer_error = None
            elif idx == failed_layer:
                layer_passed = False
                layer_error = None
            else:
                # Layers after the failing one get the same "skipped
                # due to earlier failure" marker that the real evaluator
                # emits — scorer._count_quality_passes keys off this
                # marker to avoid penalising L3 when L1/L2 broke.
                layer_passed = False
                layer_error = f"Skipped: layer {failed_layer} failed"
            layers.append(
                LayerResult(
                    layer=idx,
                    name=name,
                    passed=layer_passed,
                    details=[],
                    duration_seconds=0.0,
                    error=layer_error,
                )
            )

        merged.append(
            EvalResult(
                case_id=case_id,
                category=meta.category,
                sdk=meta.sdk,
                model=model,
                attempt=1,
                generated_code="",
                layers=layers,
                failed_at_layer=failed_layer,
                passed=cr.passed,
                total_score=1.0 if cr.passed else 0.0,
                duration_seconds=0.0,
                token_usage=TokenUsage(
                    input_tokens=0,
                    output_tokens=0,
                    total_tokens=0,
                ),
                cost_usd=0.0,
                tier=meta.tier,
                reasoning_types=meta.reasoning_types,
            )
        )

    return merged


@app.command()
def run(
    cases_dir: Annotated[
        Path,
        typer.Option("--cases", help="Path to cases directory"),
    ] = Path("cases"),
    model: Annotated[
        str,
        typer.Option("--model", "-m", help="LLM model to evaluate"),
    ] = "mock",
    category: Annotated[
        Optional[str],
        typer.Option("--category", "-c", help="Filter by category"),
    ] = None,
    difficulty: Annotated[
        Optional[str],
        typer.Option("--difficulty", "-d", help="Filter by difficulty"),
    ] = None,
    output_dir: Annotated[
        Path,
        typer.Option("--output-dir", "-o", help="Output directory for results"),
    ] = Path("results"),
    attempts: Annotated[
        int,
        typer.Option("--attempts", "-a", help="Number of attempts per case"),
    ] = 1,
    tier: Annotated[
        Optional[str],
        typer.Option(
            "--tier",
            help="Filter by tier: sanity, core, challenge (comma-separated)",
        ),
    ] = None,
    sdk: Annotated[
        Optional[str],
        typer.Option(
            "--sdk",
            help=(
                "Filter by SDK bucket (comma-separated): zephyr, "
                "embedded-linux, freertos, esp-idf, stm32-hal"
            ),
        ),
    ] = None,
    visibility: Annotated[
        str | None,
        typer.Option("--visibility", help="Filter by visibility (public/private)"),
    ] = None,
    after_date: Annotated[
        str | None,
        typer.Option(
            "--after-date",
            help="Only include cases created after this date (YYYY-MM-DD)",
        ),
    ] = None,
    feedback_rounds: Annotated[
        int,
        typer.Option(
            "--feedback-rounds", "-f", help="Compiler feedback rounds (0=disabled)"
        ),
    ] = 0,
    temperature: Annotated[
        float,
        typer.Option(
            "--temperature", "-t", help="LLM temperature (recorded in report metadata)"
        ),
    ] = 0.0,
    scenario: Annotated[
        str,
        typer.Option(
            "--scenario",
            "-s",
            help="Evaluation scenario: generation or bugfix",
        ),
    ] = "generation",
    include_private: Annotated[
        bool,
        typer.Option(
            "--include-private",
            help="Include private held-out cases (default: public only)",
        ),
    ] = False,
    private_cases: Annotated[
        Optional[Path],
        typer.Option(
            "--private-cases",
            help="Path to private cases directory (separate repo)",
        ),
    ] = None,
    retest_only: Annotated[
        bool,
        typer.Option(
            "--retest-only",
            help="Only run cases that changed since last test or were never tested",
        ),
    ] = False,
    run_id: Annotated[
        Optional[str],
        typer.Option(
            "--run-id",
            help=(
                "Distinct tag appended to the run archive directory "
                "(e.g. 'n1', 'n2') so multiple runs of the same model on "
                "the same day don't overwrite each other — required when "
                "collecting n>=2 samples for CI analysis"
            ),
        ),
    ] = None,
    context_pack: Annotated[
        Optional[str],
        typer.Option(
            "--context-pack",
            help=(
                "Path to a global context file prepended to every prompt "
                "(e.g. team's CLAUDE.md). Special value 'expert' uses the "
                "bundled expert pack at "
                "src/embedeval/context_packs/expert.md. See "
                "docs/CONTEXT-QUALITY-MODE.md."
            ),
        ),
    ] = None,
    no_think: Annotated[
        bool,
        typer.Option(
            "--no-think",
            help=(
                "Append /no_think to every prompt to disable chain-of-thought "
                "on models that support it (Qwen3, QwQ). Saves tokens on "
                "rate-limited providers."
            ),
        ),
    ] = False,
    corpus_dir: Annotated[
        Optional[Path],
        typer.Option(
            "--corpus-dir",
            help=(
                "Directory for the generation corpus cache. "
                "When set, completed cells are reused across runs "
                "(no LLM call when the key matches). "
                "Defaults to <output-dir>/corpus when not specified."
            ),
        ),
    ] = None,
    case_ids: Annotated[
        Optional[str],
        typer.Option(
            "--case-ids",
            help="Comma-separated case IDs to run (e.g. nxp-mcxc-i2c-001).",
        ),
    ] = None,
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            help=(
                "Bypass the corpus cache and regenerate all cells in scope. "
                "Overwrites existing corpus entries. "
                "Use with a case filter to force a single case."
            ),
        ),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose logging"),
    ] = False,
) -> None:
    """Run benchmark evaluation on cases."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG, force=True)

    if scenario not in ("generation", "bugfix"):
        typer.echo(f"Unknown scenario: {scenario}. Use 'generation' or 'bugfix'.")
        raise typer.Exit(code=1)

    # Context Quality Mode is wired through the generation path only.
    # bugfix.run_bugfix_benchmark calls call_model() without forwarding
    # context_pack, so allowing the flag here would silently strip the pack
    # while still recording its hash in the tracker — a data-integrity trap.
    if scenario == "bugfix" and context_pack is not None:
        typer.echo(
            "Error: --context-pack is not supported for --scenario bugfix. "
            "Use --scenario generation, or run bugfix without --context-pack.",
            err=True,
        )
        raise typer.Exit(code=1)

    from embedeval.models import CaseTier
    from embedeval.runner import Filters, run_benchmark
    from embedeval.scorer import score as score_results

    filters = Filters()
    if category:
        filters.categories = [CaseCategory(category)]
    if difficulty:
        filters.difficulties = [DifficultyTier(difficulty)]
    if tier:
        filters.tiers = [CaseTier(t.strip()) for t in tier.split(",")]
    if sdk:
        filters.sdks = _parse_sdk_filter(sdk)
    if visibility:
        filters.visibility = Visibility(visibility)
    if after_date:
        filters.after_date = after_date
    if case_ids:
        filters.case_ids = [c.strip() for c in case_ids.split(",") if c.strip()]

    # Build case_dir_map covering all discoverable cases (public + private).
    # Needed so update_tracker and generate_results_doc can hash private
    # cases correctly — without it they'd resolve to non-existent paths
    # under cases_dir and record the empty-content hash.
    from embedeval.runner import discover_cases as _discover

    case_dir_map: dict[str, Path] = {meta.id: cd for cd, meta in _discover(cases_dir)}
    if private_cases:
        for cd, meta in _discover(private_cases):
            case_dir_map[meta.id] = cd

    # Retest-only filtering
    if retest_only:
        from embedeval.result_tracker import (
            find_cases_needing_retest,
            load_tracker,
        )
        from embedeval.runner import filter_cases as _filter

        tracker = load_tracker(output_dir)
        all_cases = _discover(cases_dir)
        if private_cases:
            all_cases.extend(_discover(private_cases))
        # Apply same visibility filter that run_benchmark will use,
        # so we don't count private cases that will be excluded later
        retest_filters = Filters(
            categories=filters.categories,
            difficulties=filters.difficulties,
            tiers=filters.tiers,
            sdks=filters.sdks,
            tags=filters.tags,
            visibility=filters.visibility
            if filters.visibility is not None
            else (None if include_private else Visibility.PUBLIC),
            after_date=filters.after_date,
        )
        selected = _filter(all_cases, retest_filters)
        all_case_ids = [meta.id for _, meta in selected]
        needs_retest = find_cases_needing_retest(
            tracker,
            model,
            cases_dir,
            all_case_ids,
            case_dir_map=case_dir_map,
        )
        if not needs_retest:
            typer.echo("All cases up to date — nothing to retest.")
            raise typer.Exit(code=0)
        typer.echo(
            f"Retest: {len(needs_retest)}/{len(all_case_ids)} cases need retesting"
        )
        # Override filters to only include cases needing retest
        filters.case_ids = needs_retest

    # Resolve and load context pack (D1: prepend to every prompt; D3: hash content)
    context_pack_text: str | None = None
    context_pack_hash: str | None = None
    if context_pack is not None:
        from embedeval.context_pack import (
            ContextPackTooLargeError,
            hash_context_pack,
            resolve_context_pack,
        )

        try:
            pack_path = resolve_context_pack(context_pack)
            context_pack_text = pack_path.read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            typer.echo(f"Error: {exc}", err=True)
            raise typer.Exit(code=1) from exc
        # Empty pack would hash to a stable non-null value but produce no
        # prompt change (_build_full_prompt strips whitespace-only packs).
        # That mismatch silently poisons the tracker for future bare runs
        # in the same output_dir.
        if not context_pack_text.strip():
            typer.echo(
                f"Error: context pack file is empty or whitespace-only: {pack_path}",
                err=True,
            )
            raise typer.Exit(code=1)
        try:
            context_pack_hash = hash_context_pack(context_pack_text)
        except ContextPackTooLargeError as exc:
            typer.echo(
                f"Warning: {exc}. Continuing — long packs may dilute LLM "
                f"attention or be ignored.",
                err=True,
            )
            # Bypass the size guard but reuse the canonical hash impl
            # so cli.py and context_pack.py can't drift apart.
            from embedeval.context_pack import _hash_raw

            context_pack_hash = _hash_raw(context_pack_text)
        typer.echo(
            f"Context pack: {pack_path.name} "
            f"(hash={context_pack_hash}, {len(context_pack_text)} chars)"
        )

    typer.echo(
        f"Running benchmark: model={model}, cases={cases_dir}, scenario={scenario}"
    )

    # Build a checkpoint path so a crashed run can resume instead of
    # starting from scratch. Deleted on successful completion below.
    model_slug = model.replace("/", "_").replace(":", "_")
    ckpt_suffix = f"_{run_id}" if run_id else ""
    checkpoint_path = (
        output_dir / "runs" / f".checkpoint_{model_slug}{ckpt_suffix}.jsonl"
    )
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)

    if scenario == "bugfix":
        from embedeval.bugfix import run_bugfix_benchmark

        results = run_bugfix_benchmark(
            cases_dir=cases_dir,
            model=model,
            filters=filters,
            include_private=include_private,
        )
    else:
        extra_dirs = [private_cases] if private_cases else None
        # Default corpus_dir to <output_dir>/corpus when not explicitly set.
        effective_corpus_dir = corpus_dir if corpus_dir is not None else output_dir / "corpus"
        results = run_benchmark(
            cases_dir=cases_dir,
            model=model,
            filters=filters,
            attempts=attempts,
            feedback_rounds=feedback_rounds,
            include_private=include_private,
            extra_cases_dirs=extra_dirs,
            checkpoint_path=checkpoint_path,
            context_pack=context_pack_text,
            no_think=no_think,
            corpus_dir=effective_corpus_dir,
            temperature=temperature,
            force=force,
        )

    if not results:
        typer.echo("No results generated.")
        raise typer.Exit(code=1)

    # Merge with tracker history so the leaderboard/safe-guide reflect the
    # comprehensive per-model state, not just this run's (possibly partial)
    # slice. --retest-only runs would otherwise clobber LEADERBOARD.md
    # with the 3-case view.
    from embedeval.result_tracker import (
        generate_results_doc,
        load_tracker,
        save_tracker,
        update_tracker,
    )

    prior_tracker = load_tracker(output_dir)
    all_cases_meta = {meta.id: meta for _, meta in _discover(cases_dir)}
    if private_cases:
        for _, meta in _discover(private_cases):
            all_cases_meta[meta.id] = meta

    comprehensive_results = _build_comprehensive_results(
        results, prior_tracker, model, all_cases_meta
    )

    report = score_results(comprehensive_results)
    report.scenario = scenario
    report.temperature = temperature
    report.n_samples_per_case = attempts

    from embedeval.reporter import (
        generate_failure_report,
        generate_json,
        generate_leaderboard,
        generate_per_check_metrics,
        generate_run_archive,
        generate_safe_guide,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{model}-results.json"
    generate_json(report, json_path)

    # Leaderboard needs every known model, not just the one that just ran,
    # otherwise a Sonnet-only invocation wipes Haiku off the page.
    leaderboard_reports = [report]
    # Raw EvalResults per model — REQ-04 per-check metrics need them.
    results_by_model: dict[str, list[EvalResult]] = {model: comprehensive_results}
    for other_model in sorted(prior_tracker.results.keys()):
        if other_model == model or other_model == "mock":
            continue
        other_merged = _build_comprehensive_results(
            [], prior_tracker, other_model, all_cases_meta
        )
        if not other_merged:
            continue
        other_report = score_results(other_merged)
        other_report.scenario = scenario
        leaderboard_reports.append(other_report)
        results_by_model[other_model] = other_merged

    leaderboard_path = output_dir / "LEADERBOARD.md"
    generate_leaderboard(leaderboard_reports, leaderboard_path)

    run_dir = generate_run_archive(
        results, report, output_dir, model, run_id=run_id, no_think=no_think
    )

    # REQ-04: emit per-(TC, check, model) metrics for external consumers
    # (Hiloop's interop.leaderboard, per-rule severity auto-assignment).
    # JSON goes into the run-scoped archive so n=3 invocations produce
    # three artifacts rather than silently overwriting each other; the
    # markdown summary stays at the flat root for human browsing and
    # mirrors LEADERBOARD.md's placement.
    generate_per_check_metrics(
        results_by_model,
        output_json=run_dir / "per_check_metrics.json",
        output_md=output_dir / "LEADERBOARD_PER_CHECK.md",
        run_id=run_id,
    )
    # Failure report still lists just this run's failures — the archive
    # has the full picture, but the one-page report is most useful as
    # "what broke in *this* invocation".
    generate_failure_report(results, run_dir / "report.md", model)

    # Update tracker after building comprehensive_results so the "prior"
    # snapshot used for merging reflects the state *before* this run.
    from embedeval.result_tracker import ContextPackMismatchError

    try:
        tracker = update_tracker(
            prior_tracker,
            results,
            cases_dir,
            model,
            case_dir_map=case_dir_map,
            context_pack_hash=context_pack_hash,
        )
    except ContextPackMismatchError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    save_tracker(tracker, output_dir)
    generate_results_doc(
        tracker,
        output_dir / "TEST_RESULTS.md",
        cases_dir,
        case_dir_map=case_dir_map,
    )

    # Generate safe guide from all available runs
    guide_path = generate_safe_guide(output_dir)

    # Clean checkpoint — run succeeded, all data is persisted.
    if checkpoint_path.is_file():
        checkpoint_path.unlink()
        logger.info("Checkpoint removed: %s", checkpoint_path)

    typer.echo(f"Results: {json_path}")
    typer.echo(f"Leaderboard: {leaderboard_path}")
    typer.echo(f"Detailed: {run_dir}/")
    typer.echo(f"Tracker: {output_dir / 'test_tracker.json'}")
    if guide_path:
        typer.echo(f"Safe guide: {guide_path}")


