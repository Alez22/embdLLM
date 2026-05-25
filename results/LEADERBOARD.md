# EmbedEval Leaderboard

<!-- SCHEMA_VERSION: 1 -->


## Model Comparison

| Model | pass@1 (full) | pass@1 (quality) | 95% CI | pass@5 | Passed | Quality | Total | Samples |
|-------|---------------|------------------|--------|--------|--------|---------|-------|---------|
| groq/openai/gpt-oss-20b | 63.6% | 63.6% | [35.4%, 84.8%] | 63.6% | 7 | 7 | 11 | n=1 |
| claude-code://haiku | 59.8% | 72.0% | [52.7%, 66.5%] | 59.8% | 113 | 136 | 189 | n=1 |
| claude-code://sonnet | 70.9% | 83.6% | [64.1%, 76.9%] | 70.9% | 134 | 158 | 189 | n=1 |
| groq/llama-3.3-70b-versatile | 38.5% | 38.5% | [17.7%, 64.5%] | 38.5% | 5 | 5 | 13 | n=1 |
| groq/meta-llama/llama-4-scout-17b-16e-instruct | 18.2% | 18.2% | [5.1%, 47.7%] | 18.2% | 2 | 2 | 11 | n=1 |
| groq/openai/gpt-oss-120b | 45.5% | 45.5% | [21.3%, 72.0%] | 45.5% | 5 | 5 | 11 | n=1 |
| groq/qwen/qwen3-32b | 36.4% | 36.4% | [15.2%, 64.6%] | 36.4% | 4 | 4 | 11 | n=1 |

*pass@1 (full) = all layers must pass. pass@1 (quality) = L0+L3 only (code quality, ignoring build/runtime).*

## Tier Breakdown

| Tier | pass@1 | Passed | Total |
|------|--------|--------|-------|
| Core | 63.6% | 7 | 11 |
| Sanity (not scored) | 33.3% | 1 | 3 |
| Core | 67.3% | 66 | 98 |
| Challenge | 52.3% | 46 | 88 |
| Sanity (not scored) | 66.7% | 2 | 3 |
| Core | 76.5% | 75 | 98 |
| Challenge | 64.8% | 57 | 88 |
| Sanity (not scored) | 50.0% | 1 | 2 |
| Core | 36.4% | 4 | 11 |
| Core | 18.2% | 2 | 11 |
| Core | 45.5% | 5 | 11 |
| Core | 36.4% | 4 | 11 |

## Reasoning Type Breakdown

| Reasoning Type | pass@1 | Cases | LLM Reliability |
|----------------|--------|-------|-----------------|
| L1 API Recall | 63.6% | 11 | Expert review required |
| L2 Rule Application | 62.5% | 8 | Expert review required |
| L4 System Reasoning | 50.0% | 8 | Expert review required |
| L1 API Recall | 62.6% | 171 | Expert review required |
| L2 Rule Application | 66.4% | 110 | Expert review required |
| L3 Cross-Domain | 36.1% | 36 | Expert review required |
| L4 System Reasoning | 62.5% | 96 | Expert review required |
| L1 API Recall | 75.4% | 171 | Review recommended |
| L2 Rule Application | 76.4% | 110 | Review recommended |
| L3 Cross-Domain | 47.2% | 36 | Expert review required |
| L4 System Reasoning | 66.7% | 96 | Expert review required |
| L1 API Recall | 38.5% | 13 | Expert review required |
| L2 Rule Application | 40.0% | 10 | Expert review required |
| L4 System Reasoning | 37.5% | 8 | Expert review required |
| L1 API Recall | 18.2% | 11 | Expert review required |
| L2 Rule Application | 25.0% | 8 | Expert review required |
| L4 System Reasoning | 12.5% | 8 | Expert review required |
| L1 API Recall | 45.5% | 11 | Expert review required |
| L2 Rule Application | 50.0% | 8 | Expert review required |
| L4 System Reasoning | 50.0% | 8 | Expert review required |
| L1 API Recall | 36.4% | 11 | Expert review required |
| L2 Rule Application | 50.0% | 8 | Expert review required |
| L4 System Reasoning | 50.0% | 8 | Expert review required |

## SDK Breakdown

| SDK | pass@1 | Passed | Total | Notes |
|-----|--------|--------|-------|-------|
| freertos | 100.0% | 1 | 1 | thin bucket (n<8) |
| esp-idf | 80.0% | 4 | 5 | thin bucket (n<8) |
| stm32-hal | 50.0% | 2 | 4 | thin bucket (n<8) |
| mcuxpresso-sdk | 0.0% | 0 | 1 | thin bucket (n<8) |
| zephyr | 58.2% | 92 | 158 |  |
| embedded-linux | 71.4% | 15 | 21 |  |
| freertos | 0.0% | 0 | 1 | thin bucket (n<8) |
| esp-idf | 80.0% | 4 | 5 | thin bucket (n<8) |
| stm32-hal | 50.0% | 2 | 4 | thin bucket (n<8) |
| zephyr | 70.9% | 112 | 158 |  |
| embedded-linux | 76.2% | 16 | 21 |  |
| freertos | 0.0% | 0 | 1 | thin bucket (n<8) |
| esp-idf | 100.0% | 5 | 5 | thin bucket (n<8) |
| stm32-hal | 25.0% | 1 | 4 | thin bucket (n<8) |
| zephyr | 50.0% | 1 | 2 | thin bucket (n<8) |
| freertos | 100.0% | 1 | 1 | thin bucket (n<8) |
| esp-idf | 60.0% | 3 | 5 | thin bucket (n<8) |
| stm32-hal | 0.0% | 0 | 4 | thin bucket (n<8) |
| mcuxpresso-sdk | 0.0% | 0 | 1 | thin bucket (n<8) |
| freertos | 0.0% | 0 | 1 | thin bucket (n<8) |
| esp-idf | 20.0% | 1 | 5 | thin bucket (n<8) |
| stm32-hal | 25.0% | 1 | 4 | thin bucket (n<8) |
| mcuxpresso-sdk | 0.0% | 0 | 1 | thin bucket (n<8) |
| freertos | 0.0% | 0 | 1 | thin bucket (n<8) |
| esp-idf | 40.0% | 2 | 5 | thin bucket (n<8) |
| stm32-hal | 50.0% | 2 | 4 | thin bucket (n<8) |
| mcuxpresso-sdk | 100.0% | 1 | 1 | thin bucket (n<8) |
| freertos | 0.0% | 0 | 1 | thin bucket (n<8) |
| esp-idf | 80.0% | 4 | 5 | thin bucket (n<8) |
| stm32-hal | 0.0% | 0 | 4 | thin bucket (n<8) |
| mcuxpresso-sdk | 0.0% | 0 | 1 | thin bucket (n<8) |

## Category Results

| Category | pass@1 | Passed | Total | Status |
|----------|--------|--------|-------|--------|
| gpio-basic | 100.0% | 2 | 2 | PASS |
| networking | 50.0% | 1 | 2 | PARTIAL |
| spi-i2c | 40.0% | 2 | 5 | FAIL |
| threading | 100.0% | 1 | 1 | PASS |
| timer | 100.0% | 1 | 1 | PASS |
| adc | 50.0% | 1 | 2 | PARTIAL |
| ble | 50.0% | 4 | 8 | PARTIAL |
| boot | 100.0% | 8 | 8 | PASS |
| device-tree | 100.0% | 8 | 8 | PASS |
| dma | 9.1% | 1 | 11 | FAIL |
| gpio-basic | 100.0% | 5 | 5 | PASS |
| isr-concurrency | 30.0% | 3 | 10 | FAIL |
| kconfig | 62.5% | 5 | 8 | PARTIAL |
| linux-driver | 70.0% | 7 | 10 | PARTIAL |
| memory-opt | 20.0% | 2 | 10 | FAIL |
| networking | 80.0% | 8 | 10 | PASS |
| ota | 77.8% | 7 | 9 | PARTIAL |
| power-mgmt | 87.5% | 7 | 8 | PASS |
| pwm | 100.0% | 1 | 1 | PASS |
| security | 62.5% | 5 | 8 | PARTIAL |
| sensor-driver | 100.0% | 8 | 8 | PASS |
| spi-i2c | 66.7% | 8 | 12 | PARTIAL |
| storage | 20.0% | 2 | 10 | FAIL |
| threading | 30.8% | 4 | 13 | FAIL |
| timer | 44.4% | 4 | 9 | FAIL |
| uart | 100.0% | 2 | 2 | PASS |
| watchdog | 66.7% | 6 | 9 | PARTIAL |
| yocto | 70.0% | 7 | 10 | PARTIAL |
| adc | 100.0% | 2 | 2 | PASS |
| ble | 100.0% | 8 | 8 | PASS |
| boot | 87.5% | 7 | 8 | PASS |
| device-tree | 100.0% | 8 | 8 | PASS |
| dma | 27.3% | 3 | 11 | FAIL |
| gpio-basic | 80.0% | 4 | 5 | PASS |
| isr-concurrency | 20.0% | 2 | 10 | FAIL |
| kconfig | 87.5% | 7 | 8 | PASS |
| linux-driver | 70.0% | 7 | 10 | PARTIAL |
| memory-opt | 60.0% | 6 | 10 | PARTIAL |
| networking | 80.0% | 8 | 10 | PASS |
| ota | 77.8% | 7 | 9 | PARTIAL |
| power-mgmt | 87.5% | 7 | 8 | PASS |
| pwm | 100.0% | 1 | 1 | PASS |
| security | 37.5% | 3 | 8 | FAIL |
| sensor-driver | 100.0% | 8 | 8 | PASS |
| spi-i2c | 83.3% | 10 | 12 | PASS |
| storage | 60.0% | 6 | 10 | PARTIAL |
| threading | 30.8% | 4 | 13 | FAIL |
| timer | 88.9% | 8 | 9 | PASS |
| uart | 50.0% | 1 | 2 | PARTIAL |
| watchdog | 100.0% | 9 | 9 | PASS |
| yocto | 80.0% | 8 | 10 | PASS |
| gpio-basic | 50.0% | 1 | 2 | PARTIAL |
| kconfig | 50.0% | 1 | 2 | PARTIAL |
| networking | 50.0% | 1 | 2 | PARTIAL |
| spi-i2c | 0.0% | 0 | 5 | FAIL |
| threading | 100.0% | 1 | 1 | PASS |
| timer | 100.0% | 1 | 1 | PASS |
| gpio-basic | 50.0% | 1 | 2 | PARTIAL |
| networking | 0.0% | 0 | 2 | FAIL |
| spi-i2c | 0.0% | 0 | 5 | FAIL |
| threading | 0.0% | 0 | 1 | FAIL |
| timer | 100.0% | 1 | 1 | PASS |
| gpio-basic | 50.0% | 1 | 2 | PARTIAL |
| networking | 50.0% | 1 | 2 | PARTIAL |
| spi-i2c | 40.0% | 2 | 5 | FAIL |
| threading | 0.0% | 0 | 1 | FAIL |
| timer | 100.0% | 1 | 1 | PASS |
| gpio-basic | 50.0% | 1 | 2 | PARTIAL |
| networking | 50.0% | 1 | 2 | PARTIAL |
| spi-i2c | 20.0% | 1 | 5 | FAIL |
| threading | 0.0% | 0 | 1 | FAIL |
| timer | 100.0% | 1 | 1 | PASS |

## Layer Pass Rate Heatmap

| Model| L0 Static| L1 Build| L2 Runtime| L3 Heuristic| L4 Mutation| |
|-------|----------|----------|----------|----------|----------||
| groq/openai/gpt-oss-20b| 64%| 100%| 100%| 100%| 100%| |
| claude-code://haiku| 83%| 92%| 92%| 84%| 100%| |
| claude-code://sonnet| 95%| 98%| 89%| 86%| 100%| |
| groq/llama-3.3-70b-versatile| 46%| 100%| 100%| 83%| 100%| |
| groq/meta-llama/llama-4-scout-17b-16e-instruct| 45%| 100%| 100%| 40%| 100%| |
| groq/openai/gpt-oss-120b| 55%| 100%| 100%| 83%| 100%| |
| groq/qwen/qwen3-32b| 36%| 100%| 100%| 100%| 100%| |

## Failure Distribution

| Layer | Failures | % of Total |
|-------|----------|-----------|
| L0 Static | 2.8 | 65% |
| L1 Build | 0.1 | 2% |
| L2 Runtime | 0.2 | 4% |
| L3 Heuristic | 1.2 | 29% |
| L4 Mutation | 0.0 | 0% |

## Category Breakdown

| Category | Pass@1 | Cases |
|----------|--------|-------|
| gpio-basic | 100% | 2 |
| networking | 50% | 2 |
| spi-i2c | 40% | 5 |
| threading | 100% | 1 |
| timer | 100% | 1 |
| adc | 50% | 2 |
| ble | 50% | 8 |
| boot | 100% | 8 |
| device-tree | 100% | 8 |
| dma | 9% | 11 |
| gpio-basic | 100% | 5 |
| isr-concurrency | 30% | 10 |
| kconfig | 62% | 8 |
| linux-driver | 70% | 10 |
| memory-opt | 20% | 10 |
| networking | 80% | 10 |
| ota | 78% | 9 |
| power-mgmt | 88% | 8 |
| pwm | 100% | 1 |
| security | 62% | 8 |
| sensor-driver | 100% | 8 |
| spi-i2c | 67% | 12 |
| storage | 20% | 10 |
| threading | 31% | 13 |
| timer | 44% | 9 |
| uart | 100% | 2 |
| watchdog | 67% | 9 |
| yocto | 70% | 10 |
| adc | 100% | 2 |
| ble | 100% | 8 |
| boot | 88% | 8 |
| device-tree | 100% | 8 |
| dma | 27% | 11 |
| gpio-basic | 80% | 5 |
| isr-concurrency | 20% | 10 |
| kconfig | 88% | 8 |
| linux-driver | 70% | 10 |
| memory-opt | 60% | 10 |
| networking | 80% | 10 |
| ota | 78% | 9 |
| power-mgmt | 88% | 8 |
| pwm | 100% | 1 |
| security | 38% | 8 |
| sensor-driver | 100% | 8 |
| spi-i2c | 83% | 12 |
| storage | 60% | 10 |
| threading | 31% | 13 |
| timer | 89% | 9 |
| uart | 50% | 2 |
| watchdog | 100% | 9 |
| yocto | 80% | 10 |
| gpio-basic | 50% | 2 |
| kconfig | 50% | 2 |
| networking | 50% | 2 |
| spi-i2c | 0% | 5 |
| threading | 100% | 1 |
| timer | 100% | 1 |
| gpio-basic | 50% | 2 |
| networking | 0% | 2 |
| spi-i2c | 0% | 5 |
| threading | 0% | 1 |
| timer | 100% | 1 |
| gpio-basic | 50% | 2 |
| networking | 50% | 2 |
| spi-i2c | 40% | 5 |
| threading | 0% | 1 |
| timer | 100% | 1 |
| gpio-basic | 50% | 2 |
| networking | 50% | 2 |
| spi-i2c | 20% | 5 |
| threading | 0% | 1 |
| timer | 100% | 1 |

## Cross-Benchmark Comparison

| Model | HumanEval | SWE-bench | EmbedEval (full) | EmbedEval (quality) | Embed Gap |
|-------|-----------|-----------|------------------|---------------------|-----------|
| claude-code://haiku | 84.0% | 48.2% | 59.8% | 72.0% | -24.2%p |
| claude-code://sonnet | 93.7% | 72.2% | 70.9% | 83.6% | -22.8%p |

*Embed Gap = EmbedEval pass@1 - HumanEval. Negative = harder than general coding.*
