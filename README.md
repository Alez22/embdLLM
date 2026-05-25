# EmbedEval

**Benchmark for evaluating LLMs on embedded firmware tasks.**

Embedded firmware development has specific requirements that general-purpose coding benchmarks
do not capture: hardware abstraction layers, peripheral initialization sequences, timing
constraints, ISR safety, memory layout, and SDK-specific API conventions. A model that scores
well on LeetCode or HumanEval may still produce dangerous firmware code that compiles cleanly
but silently violates hardware constraints.

This project measures that gap — across both frontier models (GPT-4, Claude, Gemini) and
open-weight models deployable on local hardware (Llama, Qwen, Mistral, DeepSeek).

---

## The Core Question

> **Can open-weight models running locally match frontier models on embedded firmware tasks?**

This matters because production firmware often cannot leave private infrastructure.
If a 70B open-weight model running on-premise reaches 80% of GPT-4's accuracy on real
firmware tasks, the trade-off is acceptable. If it reaches 40%, it is not.
This benchmark gives a data-driven answer.

---

## What Makes Embedded Different

Standard coding benchmarks miss the implicit knowledge embedded engineers carry:

```
Prompt:  "Implement an I2C master read from register 0x75 on device 0x68.
          Use the MCUXpresso SDK. Handle communication errors."

What the model must know without being told:
  — Enable the peripheral clock before calling I2C_MasterInit()
  — Configure pin mux before peripheral use
  — Use 7-bit address format (SDK shifts internally — 0x68, not 0xD0)
  — Check the return value of I2C_MasterTransferBlocking()
  — Set kI2C_TransferDefaultFlag in the transfer struct
```

A model that gets this right without hints has real domain knowledge.
A model that needs explicit guidance is not safe to use on production firmware.

Every prompt in this benchmark states **what** to build, never **how** to make it correct.
The checks verify knowledge the model must bring from its training data.

---

## Evaluation Layers

Each case runs up to five evaluation layers, stopping at the first failure:

| Layer | Name | What it checks |
|-------|------|----------------|
| L0 | Static analysis | Required headers, APIs, anti-hallucination patterns |
| L1 | Compile gate | Code compiles for the target (Docker, SDK toolchain) |
| L2 | Runtime execution | Correct behavior on native simulator |
| L3 | Static heuristic | Implicit knowledge: ordering, safety, SDK conventions |
| L4 | Mutation proof | Test suite catches seeded bugs |

L1 requires Docker with the target SDK. L1-skip cases (bare-metal, no RTOS) run L0+L3 only.

---

## Task Types

| Type | Description | Grading |
|------|-------------|---------|
| Generation | Write firmware from spec | Automated |
| Bug detection | Find a seeded bug | Automated |
| Refactoring | Reduce complexity, preserve behavior | Automated (lizard + regression) |
| Documentation | Generate Doxygen headers | Automated + human review |
| Test generation | Write unit tests for a module | Automated (compile + mutation coverage) |
| Architecture | Design a system component | Human review |

---

## SDK Coverage

Cases exist for the following SDKs and platforms:

| SDK | Platforms | Cases |
|-----|-----------|-------|
| Zephyr RTOS | nRF52, STM32, native_sim | upstream |
| ESP-IDF | ESP32 | upstream |
| STM32 HAL | STM32F4, STM32H7 | upstream |
| FreeRTOS | generic Cortex-M | upstream |
| Linux kernel | drivers, sysfs | upstream |
| MCUXpresso SDK | MCXC144 (M0+), RT1170 (M7+M4) | this repo |

---

## Model Strategy

**Phase 1 — Benchmark via cloud APIs.**
Run the same model weights through Groq/OpenRouter without local hardware.

| Provider | Models |
|----------|--------|
| Groq | llama-3.3-70b-versatile, qwen3-32b |
| OpenRouter | devstral, qwen3-coder, deepseek-v3 |
| Anthropic | claude-sonnet-4.6, claude-opus-4 (reference ceiling) |

**Phase 2 — Deploy the winner locally via Ollama.**
Benchmark results transfer directly — same weights, same scores.
The only variable that changes is latency and privacy.

---

## Getting Started

```bash
# Install
uv sync

# Run with a mock model (no API key needed)
uv run embedeval run --model mock --cases cases/

# Run against Groq (free tier)
export GROQ_API_KEY=your_key_here
uv run embedeval run \
  --model groq/llama-3.3-70b-versatile \
  --cases cases/ \
  --attempts 3

# Open the results dashboard
uv run embedeval dashboard
```

---

## Results Dashboard

```bash
uv run embedeval dashboard
# → http://localhost:7860
```

Leaderboard shows models ranked by pass rate, broken down by difficulty (Easy / Medium / Hard).
Each cell links to a detailed view with check results and a diff against the reference solution.

---

## Adding Cases

Cases follow a simple directory layout:

```
cases/<sdk-bucket>/<case-id>/
├── metadata.yaml     # id, platform, sdk, difficulty, tier, tags
├── prompt.md         # what to build — never how to make it safe
├── reference/
│   └── main.c        # correct implementation
└── checks/
    ├── static.py     # L0: required headers, APIs, no hallucination
    └── behavior.py   # L3: implicit knowledge, ordering, safety
```

The prompt must state what to build, never mention safety requirements, clock enables,
address formats, or any other knowledge the model is expected to have.

---

## Relation to Upstream

Built on top of [EmbedEval](https://github.com/Ecro/embedeval), which covers Zephyr,
ESP-IDF, STM32 HAL, FreeRTOS, and Linux. Upstream cases are preserved unchanged.
New cases follow the identical format and can be contributed upstream via PR.
