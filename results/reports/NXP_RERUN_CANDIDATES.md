# NXP Re-Run Candidates — `attempts=5`

Models worth a **fresh 24-case NXP run at `attempts=5`**. They are excluded from
`PERFORMANCE_REPORT.md`'s NXP chart (which shows a5 rows only) either because their
best result came from an `attempts=1` probe, or because their existing a5 run looks
anomalous, or because they were never tested on NXP at all.

Cases live in `cases/mcuxpresso-sdk/` (24 cases). All commands need the provider API
keys from `.env` at the project root.

## Candidates

- [ ] **`openrouter/qwen/qwen3-235b-a22b-2507`** — best full-set @a1 (8/24 = 33%),
  but its only a5 run scored 0/24. The a1→a5 collapse is suspicious; reconfirm.
- [ ] **`openrouter/anthropic/claude-opus-4.8`** — 4/6 @a1 but only ever covered
  6 of 24 cases (six 2-case probe runs). Never run on the full set or at a5.
- [ ] **`openrouter/anthropic/claude-sonnet-4.6`** — 0% pass but high avg_score
  (near-miss code), and it is the agent-mode winner. Deserves a proper a5 run.
- [ ] **`openrouter/deepseek/deepseek-v4-flash`** — 5/24 @a1, but the a5 run
  collapsed to 1/24. Reconfirm with a clean a5 run.
- [ ] **`openrouter/deepseek/deepseek-v4-pro`** — only one a1 run (1/24); never a5.
- [ ] **`openrouter/z-ai/glm-4.7-flash`** — present only on Zephyr; never tested
  on NXP at all.

## Command template

```bash
uv run embedeval run \
  --model <MODEL_ID> \
  --cases cases/mcuxpresso-sdk/ \
  --attempts 5
```

Example:

```bash
uv run embedeval run \
  --model openrouter/qwen/qwen3-235b-a22b-2507 \
  --cases cases/mcuxpresso-sdk/ \
  --attempts 5
```

After the runs, regenerate the report:

```bash
uv run python results/gen_performance_report.py
```
