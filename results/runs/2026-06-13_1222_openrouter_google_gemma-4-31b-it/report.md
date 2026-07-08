# Benchmark Report: openrouter/google/gemma-4-31b-it

**Date:** 2026-06-13 12:22 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/google/gemma-4-31b-it |
| Total Cases | 55 |
| Passed | 8 |
| Failed | 47 |
| pass@1 | 14.5% |

## Failed Cases (47)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `dma-001` | dma | static_analysis | dma_header_included, dma_block_config_struct |
| `dma-001` | dma | static_analysis | dma_block_config_struct |
| `dma-001` | dma | static_analysis | dma_block_config_struct |
| `dma-001` | dma | static_heuristic | memory_to_memory_direction |
| `dma-002` | dma | static_analysis | peripheral_to_memory_direction |
| `dma-002` | dma | static_analysis | peripheral_to_memory_direction, dma_config_called |
| `dma-002` | dma | static_analysis | peripheral_to_memory_direction, dma_config_struct |
| `dma-002` | dma | static_analysis | peripheral_to_memory_direction, dma_config_called |
| `dma-002` | dma | static_analysis | peripheral_to_memory_direction, dma_config_struct, dma_config_called |
| `dma-003` | dma | static_analysis | cyclic_flag_set, dma_reload_called, dma_stop_called, dma_config_and_start |
| `dma-003` | dma | static_analysis | dma_header_included, cyclic_flag_set, dma_reload_called, dma_stop_called, dma_config_and_start |
| `dma-003` | dma | static_analysis | cyclic_flag_set, dma_reload_called, dma_stop_called, dma_config_and_start |
| `dma-003` | dma | static_analysis | cyclic_flag_set, dma_reload_called |
| `dma-003` | dma | static_analysis | dma_header_included, cyclic_flag_set, dma_reload_called, dma_stop_called, dma_config_and_start |
| `dma-004` | dma | static_analysis | next_block_pointer_used, block_count_set, head_block_set, multiple_block_descriptors |
| `dma-004` | dma | static_analysis | block_count_set, head_block_set, multiple_block_descriptors |
| `dma-004` | dma | static_analysis | dma_header_included, next_block_pointer_used, head_block_set, multiple_block_descriptors |
| `dma-004` | dma | static_analysis | next_block_pointer_used, head_block_set, multiple_block_descriptors |
| `dma-004` | dma | static_analysis | next_block_pointer_used, block_count_set, head_block_set, multiple_block_descriptors |
| `dma-005` | dma | static_analysis | cache_header_included |
| `dma-005` | dma | static_analysis | cache_header_included, cache_invalidate_present |
| `dma-005` | dma | static_analysis | cache_header_included, cache_invalidate_present |
| `dma-005` | dma | static_analysis | cache_header_included, cache_invalidate_present |
| `dma-005` | dma | static_analysis | cache_header_included |
| `dma-006` | dma | static_analysis | dma_header_included |
| `dma-007` | dma | static_analysis | channel_priority_field_used |
| `dma-007` | dma | static_analysis | channel_priority_field_used |
| `dma-007` | dma | static_analysis | channel_priority_field_used |
| `dma-007` | dma | static_analysis | channel_priority_field_used |
| `dma-007` | dma | static_analysis | channel_priority_field_used |
| `dma-008` | dma | static_analysis | volatile_error_flag |
| `dma-008` | dma | static_heuristic | error_flag_is_volatile, callback_sets_flag_on_error_status, error_flag_causes_return, error_flag_read_after_sync |
| `dma-009` | dma | static_heuristic | dma_start_called_twice |
| `dma-009` | dma | static_analysis | dma_header_included, kernel_header_included |
| `dma-009` | dma | static_heuristic | timeout_mechanism_present, dma_start_called_twice |
| `dma-009` | dma | static_analysis | kernel_header_included |
| `dma-009` | dma | static_heuristic | dma_start_called_twice |
| `dma-011` | dma | static_analysis | three_block_configs, blocks_linked, head_block_set |
| `dma-011` | dma | static_analysis | three_block_configs, blocks_linked |
| `dma-011` | dma | static_analysis | three_block_configs, block_count_three, head_block_set |
| `dma-011` | dma | static_analysis | three_block_configs, blocks_linked |
| `dma-011` | dma | static_analysis | three_block_configs, blocks_linked, block_count_three, head_block_set |
| `dma-012` | dma | static_analysis | dma_header_included, cache_flush_before_dma |
| `dma-012` | dma | static_heuristic | wait_for_completion |
| `dma-012` | dma | static_heuristic | wait_for_completion |
| `dma-012` | dma | static_analysis | cache_flush_before_dma |
| `dma-012` | dma | static_heuristic | wait_for_completion |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `head_block_set` | 8 | dma-004, dma-004, dma-004, dma-004, dma-004 (+3 more) |
| `dma_header_included` | 7 | dma-001, dma-003, dma-003, dma-004, dma-006 (+2 more) |
| `peripheral_to_memory_direction` | 5 | dma-002, dma-002, dma-002, dma-002, dma-002 |
| `cyclic_flag_set` | 5 | dma-003, dma-003, dma-003, dma-003, dma-003 |
| `dma_reload_called` | 5 | dma-003, dma-003, dma-003, dma-003, dma-003 |
| `multiple_block_descriptors` | 5 | dma-004, dma-004, dma-004, dma-004, dma-004 |
| `cache_header_included` | 5 | dma-005, dma-005, dma-005, dma-005, dma-005 |
| `channel_priority_field_used` | 5 | dma-007, dma-007, dma-007, dma-007, dma-007 |
| `three_block_configs` | 5 | dma-011, dma-011, dma-011, dma-011, dma-011 |
| `dma_stop_called` | 4 | dma-003, dma-003, dma-003, dma-003 |
| `dma_config_and_start` | 4 | dma-003, dma-003, dma-003, dma-003 |
| `next_block_pointer_used` | 4 | dma-004, dma-004, dma-004, dma-004 |
| `blocks_linked` | 4 | dma-011, dma-011, dma-011, dma-011 |
| `dma_block_config_struct` | 3 | dma-001, dma-001, dma-001 |
| `dma_config_called` | 3 | dma-002, dma-002, dma-002 |
| `block_count_set` | 3 | dma-004, dma-004, dma-004 |
| `cache_invalidate_present` | 3 | dma-005, dma-005, dma-005 |
| `dma_start_called_twice` | 3 | dma-009, dma-009, dma-009 |
| `wait_for_completion` | 3 | dma-012, dma-012, dma-012 |
| `dma_config_struct` | 2 | dma-002, dma-002 |
| `kernel_header_included` | 2 | dma-009, dma-009 |
| `block_count_three` | 2 | dma-011, dma-011 |
| `cache_flush_before_dma` | 2 | dma-012, dma-012 |
| `memory_to_memory_direction` | 1 | dma-001 |
| `volatile_error_flag` | 1 | dma-008 |
| `error_flag_is_volatile` | 1 | dma-008 |
| `callback_sets_flag_on_error_status` | 1 | dma-008 |
| `error_flag_causes_return` | 1 | dma-008 |
| `error_flag_read_after_sync` | 1 | dma-008 |
| `timeout_mechanism_present` | 1 | dma-009 |

## TC Improvement Suggestions

