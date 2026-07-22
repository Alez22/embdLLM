"""Tests for the agent leaderboard aggregation (agent_summary)."""

import json
from pathlib import Path

from embedeval.agent_summary import build_leaderboard


def _write_run(
    results_dir: Path,
    run_id: str,
    model: str,
    *,
    l1_check: str,
    cases: list[tuple[str, int | None]],
    total_tokens: int = 1000,
) -> None:
    """@brief Write a minimal agent_run.json.

    @param l1_check Name of the L1 layer's check — 'nxp_gcc' marks a real
        container run, 'nxp_available' marks a host soft-skip (excluded).
    @param cases List of (case_id, passed_at_turn); passed_at_turn None = fail.
    """
    run_dir = results_dir / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    case_objs = []
    for case_id, passed_turn in cases:
        case_objs.append(
            {
                "case_id": case_id,
                "passed": passed_turn is not None,
                "turns_used": passed_turn or 5,
                "passed_at_turn": passed_turn,
                "history": [
                    {"layers": [{"layer": 1, "details": [{"check_name": l1_check}]}]}
                ],
            }
        )
    payload = {
        "model": model,
        "max_turns": 5,
        "context_pack": "nxp.md",
        "cases": case_objs,
        "summary": {
            "recovery_rate": 0.5,
            "total_cost_usd": 0.0,
            "total_tokens": total_tokens,
        },
    }
    (run_dir / "agent_run.json").write_text(json.dumps(payload), encoding="utf-8")


def test_leaderboard_ranks_and_excludes_host_runs(tmp_path: Path) -> None:
    """Container runs are ranked by pass count; host-mode runs are dropped."""
    # Container run: glm passes both cases.
    _write_run(
        tmp_path,
        "2026-01-01_0000_openrouter_z-ai_glm-5.2_t5",
        "openrouter/z-ai/glm-5.2",
        l1_check="nxp_gcc",
        cases=[("nxp-mcxc-gpio-001", 2), ("nxp-rt1170-dma-001", 3)],
    )
    # Container run: deepseek passes only one.
    _write_run(
        tmp_path,
        "2026-01-01_0001_openrouter_deepseek_deepseek-v4-flash_t5",
        "openrouter/deepseek/deepseek-v4-flash",
        l1_check="nxp_gcc",
        cases=[("nxp-mcxc-gpio-001", 1), ("nxp-rt1170-dma-001", None)],
    )
    # Host-mode run: must be excluded entirely despite passing everything.
    _write_run(
        tmp_path,
        "2026-01-01_0002_openrouter_qwen_qwen3-32b_t5",
        "openrouter/qwen/qwen3-32b",
        l1_check="nxp_available",
        cases=[("nxp-mcxc-gpio-001", 1), ("nxp-rt1170-dma-001", 1)],
    )

    rows = build_leaderboard(tmp_path)

    # Host-mode qwen dropped; only the two container runs remain.
    assert [r.model for r in rows] == [
        "openrouter/z-ai/glm-5.2",
        "openrouter/deepseek/deepseek-v4-flash",
    ]
    # Ranked by pass count: glm (2) before deepseek (1).
    assert rows[0].passed == 2
    assert rows[1].passed == 1
    # passed_at_turn is carried through for the RT1170 discriminator table.
    assert rows[0].passed_at_turn["nxp-rt1170-dma-001"] == 3
    assert rows[1].passed_at_turn["nxp-rt1170-dma-001"] is None


def test_equal_pass_tie_break_prefers_fewer_tokens(tmp_path: Path) -> None:
    """With cost unreported (0), the cheaper run by tokens ranks first."""
    _write_run(
        tmp_path,
        "2026-01-01_0000_openrouter_qwen_qwen3.6-plus_t5",
        "openrouter/qwen/qwen3.6-plus",
        l1_check="nxp_gcc",
        cases=[("nxp-mcxc-gpio-001", 1)],
        total_tokens=300_000,
    )
    _write_run(
        tmp_path,
        "2026-01-01_0001_openrouter_deepseek_deepseek-v4-flash_t5",
        "openrouter/deepseek/deepseek-v4-flash",
        l1_check="nxp_gcc",
        cases=[("nxp-mcxc-gpio-001", 1)],
        total_tokens=200_000,
    )
    rows = build_leaderboard(tmp_path)
    assert [r.model for r in rows] == [
        "openrouter/deepseek/deepseek-v4-flash",
        "openrouter/qwen/qwen3.6-plus",
    ]


def test_open_weight_flag(tmp_path: Path) -> None:
    """Cloud-only vendors (anthropic) are flagged as not locally deployable."""
    _write_run(
        tmp_path,
        "2026-01-01_0000_openrouter_anthropic_claude-sonnet-4.6_t5",
        "openrouter/anthropic/claude-sonnet-4.6",
        l1_check="nxp_gcc",
        cases=[("nxp-mcxc-gpio-001", 1)],
    )
    _write_run(
        tmp_path,
        "2026-01-01_0001_openrouter_z-ai_glm-5.2_t5",
        "openrouter/z-ai/glm-5.2",
        l1_check="nxp_gcc",
        cases=[("nxp-mcxc-gpio-001", 1)],
    )
    rows = build_leaderboard(tmp_path)
    by_model = {r.model: r for r in rows}
    assert by_model["openrouter/anthropic/claude-sonnet-4.6"].is_open_weight is False
    assert by_model["openrouter/z-ai/glm-5.2"].is_open_weight is True
