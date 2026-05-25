# embedeval-nxp

**LLM benchmark for NXP bare-metal firmware development.**

Fork/extension of [EmbedEval](https://github.com/Ecro/embedeval) adding NXP MCUXpresso SDK
cases, new task types absent from the upstream project, and a human-in-the-loop review workflow.

---

## Why This Exists

Upstream EmbedEval covers Zephyr, ESP-IDF, STM32 HAL, FreeRTOS, Linux kernel.
**NXP bare-metal is completely absent.** For audio amplifier firmware development on
Kinetis/MCX platforms with MCUXpresso SDK, this gap makes the upstream benchmark
useless for deciding which local LLM to deploy.

Secondary goal: evaluate task types that upstream ignores entirely — refactoring,
documentation generation (Doxygen), code explanation, and architectural reasoning.
These are high-value for daily firmware work but require human judgment to grade.

---

## Getting Started

### 1. Fork the upstream repo

Go to https://github.com/Ecro/embedeval and click **Fork** (top-right).
This creates your own copy under `github.com/YOUR_USERNAME/embedeval`.

### 2. Clone your fork locally

```bash
# Replace YOUR_USERNAME with your GitHub username
git clone https://github.com/YOUR_USERNAME/embedeval.git embedeval-nxp
cd embedeval-nxp
```

### 3. Install and validate

```bash
# Install dependencies
uv sync

# Validate that upstream cases work (optional)
uv run embedeval validate --cases cases/zephyr/ --category isr-concurrency

# Test the pipeline with a mock model (free, no API key)
uv run embedeval run --model mock --cases cases/zephyr/isr-concurrency-001/
```

---

## Key Design Principle: Implicit Knowledge

Prompts state **what** to build, never **how** to make it safe.

```
Prompt:  "Implement an I2C master read from register 0x75 on device 0x68.
          Use NXP MCUXpresso SDK for MCXC144. Handle communication errors."

What an embedded engineer knows (not in prompt):
  - CLOCK_EnableClock() before I2C_MasterInit()
  - PORT_SetPinMux() before peripheral use
  - Address must be left-shifted for 8-bit format (0x68 << 1)
  - I2C_MasterTransferBlocking() return value must be checked
  - kI2C_TransferDefaultFlag for standard transfers
```

A model that writes correct code without being told these things has real domain knowledge.
A model that needs explicit hints is not safe to use unsupervised on production firmware.

---

## Task Types

This project covers task types missing from all existing embedded LLM benchmarks:

| Type | Description | Grading |
|------|-------------|---------|
| Generation | Write firmware from spec (implicit) | Automated (compile + checks) |
| Bug detection | Find bug in seeded-mutation code | Automated (mutation pass/fail) |
| Refactoring | Reduce complexity/stack, preserve behavior | Automated (lizard + regression) |
| Documentation | Generate Doxygen headers | Human review + LLM pre-screen |
| Explanation | Explain legacy/obfuscated code | Human review + LLM pre-screen |
| Test generation | Write Unity tests for a module | Automated (compile + mutation coverage) |
| Architecture | Design a system (e.g. power-safe flash) | Human review + LLM pre-screen |

---

## Human Review Workflow

For subjective tasks, an LLM pre-screener (Opus/Sonnet) analyzes the output
and produces a structured critique before the human reviews it.

```
model output → LLM pre-analysis (JSON) → human confirms/overrides scores
```

This halves review time: the LLM handles reading and initial assessment,
the human handles final judgment on correctness and domain accuracy.

---

## Model Strategy

**Phase 1 — Benchmark now (cloud APIs):**
Same model weights, no local hardware needed yet.

| Provider | Models | Notes |
|----------|--------|-------|
| Groq | llama-3.3-70b-versatile, qwen-qwq-32b | Free tier, fast |
| OpenRouter | devstral, qwen3-coder, deepseek-v3 | Wider selection |
| Anthropic | claude-opus-4, claude-sonnet-4.6 | Reference ceiling |

**Phase 2 — Deploy locally (Ollama):**
Once dedicated hardware is available, redeploy the winner from Phase 1.
Benchmark results transfer directly — same weights, same scores.

---

## Getting Started

### 1. Fork the upstream repo

Go to https://github.com/Ecro/embedeval and click **Fork** (top-right).
This creates your own copy under `github.com/YOUR_USERNAME/embedeval`.

### 2. Clone your fork locally

```bash
# Replace YOUR_USERNAME with your GitHub username
git clone https://github.com/YOUR_USERNAME/embedeval.git embedeval-nxp
cd embedeval-nxp

# (optional) Rename the remote to distinguish your fork
git remote rename origin my-fork
```

### 3. Install and validate

```bash
# Install dependencies and activate environment
uv sync

# Validate all reference solutions pass their checks
uv run embedeval validate --cases cases/nxp-bare-metal/

# Run benchmark against a model (mock = no API key needed)
uv run embedeval run --model mock --cases cases/nxp-bare-metal/

# Run against Groq (free tier)
export GROQ_API_KEY=your_key_here
uv run embedeval run \
  --model groq/llama-3.3-70b-versatile \
  --cases cases/nxp-bare-metal/ \
  --attempts 3

# Human review of subjective tasks
uv run embedeval review \
  --cases cases/nxp-bare-metal/ \
  --reviewer-model anthropic/claude-opus-4-20250514
```

---

## NXP Case Categories

| Category | Target Knowledge |
|----------|-----------------|
| nxp-gpio | GPIO init, pin mux, IRQ, clock gate |
| nxp-i2c | I2C master/slave, address format, error handling |
| nxp-spi | SPI master, CS manual control, transfer sequences |
| nxp-uart | UART async TX/RX, ring buffer, baud config |
| nxp-dma | DMA transfer, completion callback, channel config |
| nxp-timer | Periodic interrupt, callback safety, reload |
| nxp-isr | ISR-safe shared data, volatile, __DSB, atomic |
| nxp-flash | Flash lifecycle, erase/write/verify, power-loss safety |
| nxp-watchdog | WDT feed timing, reset handling |
| nxp-lowpower | Sleep mode entry, wakeup sources, peripheral shutdown |

---

## Relation to Upstream EmbedEval

This project is a fork, not a replacement. Upstream STM32/FreeRTOS/Zephyr cases are
preserved. NXP cases follow the identical case format (metadata.yaml + prompt.md +
checks/) so they could eventually be contributed upstream via PR.
