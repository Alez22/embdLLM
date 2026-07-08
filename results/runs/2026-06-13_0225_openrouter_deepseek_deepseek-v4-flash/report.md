# Benchmark Report: openrouter/deepseek/deepseek-v4-flash

**Date:** 2026-06-13 02:25 UTC

## Summary

| Metric | Value |
|--------|-------|
| Model | openrouter/deepseek/deepseek-v4-flash |
| Total Cases | 790 |
| Passed | 549 |
| Failed | 241 |
| pass@1 | 69.5% |

## Failed Cases (241)

| Case | Difficulty | Failed Layer | Failed Checks |
|------|-----------|-------------|--------------|
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |
| `adc-002` | adc | static_heuristic | sample_buffer_nonzero |
| `ble-005` | ble | static_heuristic | auth_cb_before_advertising |
| `ble-006` | ble | static_heuristic | auth_state_reset_on_disconnect |
| `ble-006` | ble | static_heuristic | auth_state_reset_on_disconnect |
| `ble-006` | ble | static_heuristic | auth_state_reset_on_disconnect |
| `ble-006` | ble | static_heuristic | auth_state_reset_on_disconnect |
| `ble-006` | ble | static_heuristic | security_set_in_connected_cb, auth_state_reset_on_disconnect |
| `ble-008` | ble | static_heuristic | bt_enable_before_scan |
| `ble-008` | ble | static_heuristic | bt_enable_before_scan, discovery_after_connected |
| `ble-008` | ble | static_heuristic | conn_cleanup_on_failed_connect |
| `ble-008` | ble | static_heuristic | conn_cleanup_on_failed_connect |
| `boot-001` | boot | static_heuristic | img_manager_dependency |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-001` | device-tree | static_heuristic | interrupt_gpio_present |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-003` | device-tree | static_heuristic | pwm_polarity_specified |
| `device-tree-005` | device-tree | static_heuristic | two_gpio_pins_configured |
| `dma-001` | dma | static_analysis | dma_header_included |
| `dma-002` | dma | static_heuristic | source_addr_fixed, dest_addr_increments |
| `dma-002` | dma | static_analysis | peripheral_to_memory_direction |
| `dma-002` | dma | static_analysis | dma_header_included, dma_start_called |
| `dma-002` | dma | static_analysis | dma_header_included |
| `dma-002` | dma | static_analysis | dma_header_included, peripheral_to_memory_direction |
| `dma-003` | dma | static_analysis | cyclic_flag_set, dma_reload_called |
| `dma-003` | dma | static_analysis | dma_header_included, cyclic_flag_set, dma_reload_called |
| `dma-003` | dma | static_analysis | dma_header_included, cyclic_flag_set, dma_reload_called |
| `dma-003` | dma | static_analysis | cyclic_flag_set, dma_reload_called |
| `dma-003` | dma | static_analysis | cyclic_flag_set |
| `dma-004` | dma | static_analysis | multiple_block_descriptors |
| `dma-004` | dma | static_analysis | multiple_block_descriptors |
| `dma-004` | dma | static_analysis | multiple_block_descriptors |
| `dma-004` | dma | static_analysis | dma_header_included, next_block_pointer_used, multiple_block_descriptors |
| `dma-004` | dma | static_analysis | dma_header_included, next_block_pointer_used, multiple_block_descriptors |
| `dma-005` | dma | static_heuristic | config_before_start |
| `dma-006` | dma | static_analysis | dma_header_included |
| `dma-006` | dma | static_analysis | dma_header_included, aligned_attribute_present |
| `dma-006` | dma | static_analysis | dma_header_included |
| `dma-007` | dma | static_analysis | dma_header_included, channel_priority_field_used |
| `dma-007` | dma | static_analysis | dma_header_included |
| `dma-007` | dma | static_analysis | channel_priority_field_used |
| `dma-007` | dma | static_analysis | dma_header_included, two_dma_config_calls, two_dma_start_calls |
| `dma-007` | dma | static_analysis | channel_priority_field_used |
| `dma-008` | dma | static_heuristic | error_flag_is_volatile, error_flag_checked_after_wait, callback_sets_flag_on_error_status, error_flag_causes_return, error_flag_read_after_sync |
| `dma-008` | dma | static_heuristic | error_flag_is_volatile, error_flag_checked_after_wait, callback_sets_flag_on_error_status, error_flag_causes_return, error_flag_read_after_sync |
| `dma-008` | dma | static_heuristic | error_flag_is_volatile, callback_sets_flag_on_error_status, error_flag_causes_return, error_flag_read_after_sync |
| `dma-008` | dma | static_heuristic | error_flag_is_volatile, callback_sets_flag_on_error_status, error_flag_causes_return, error_flag_read_after_sync |
| `dma-009` | dma | static_heuristic | dma_config_after_stop, dma_start_called_twice |
| `dma-009` | dma | static_heuristic | dma_start_called_twice |
| `dma-009` | dma | static_heuristic | dma_config_after_stop, timeout_mechanism_present, dma_start_called_twice |
| `dma-009` | dma | static_analysis | dma_header_included |
| `dma-009` | dma | static_analysis | dma_header_included |
| `dma-011` | dma | static_analysis | three_block_configs |
| `dma-011` | dma | static_analysis | three_block_configs, blocks_linked |
| `dma-011` | dma | static_analysis | three_block_configs, blocks_linked |
| `dma-011` | dma | static_analysis | three_block_configs, blocks_linked, block_count_three, head_block_set |
| `dma-011` | dma | static_analysis | three_block_configs |
| `dma-012` | dma | static_heuristic | device_ready_check |
| `dma-012` | dma | static_analysis | dma_header_included, cache_flush_before_dma |
| `dma-012` | dma | static_heuristic | wait_for_completion |
| `dma-012` | dma | static_analysis | cache_flush_before_dma, direction_memory_to_memory |
| `isr-concurrency-001` | isr-concurrency | static_analysis | no_printk |
| `isr-concurrency-001` | isr-concurrency | static_analysis | zephyr_headers_included |
| `isr-concurrency-002` | isr-concurrency | static_heuristic | no_forbidden_apis_in_isr |
| `isr-concurrency-002` | isr-concurrency | static_analysis | no_printk_in_isr |
| `isr-concurrency-002` | isr-concurrency | static_heuristic | no_forbidden_apis_in_isr |
| `isr-concurrency-002` | isr-concurrency | static_heuristic | consumer_uses_k_forever, no_forbidden_apis_in_isr |
| `isr-concurrency-002` | isr-concurrency | static_heuristic | message_struct_defined, no_forbidden_apis_in_isr |
| `isr-concurrency-005` | isr-concurrency | static_analysis | init_before_isr_call |
| `isr-concurrency-005` | isr-concurrency | static_analysis | k_work_declared, k_work_init_called, k_work_submit_called, work_handler_correct_signature, init_before_isr_call |
| `isr-concurrency-005` | isr-concurrency | static_analysis | init_before_isr_call |
| `isr-concurrency-005` | isr-concurrency | static_heuristic | work_handler_does_processing |
| `isr-concurrency-005` | isr-concurrency | static_heuristic | work_handler_does_processing |
| `isr-concurrency-006` | isr-concurrency | static_analysis | fifo_reserved_field |
| `isr-concurrency-006` | isr-concurrency | static_analysis | fifo_reserved_field |
| `isr-concurrency-006` | isr-concurrency | static_heuristic | k_fifo_get_not_in_isr, no_forbidden_apis_in_isr |
| `isr-concurrency-006` | isr-concurrency | static_heuristic | no_forbidden_apis_in_isr |
| `isr-concurrency-007` | isr-concurrency | static_heuristic | high_priority_lower_number |
| `isr-concurrency-008` | isr-concurrency | static_heuristic | memory_barrier_present, barrier_between_data_and_index_update |
| `isr-concurrency-008` | isr-concurrency | static_heuristic | memory_barrier_present, barrier_between_data_and_index_update |
| `isr-concurrency-008` | isr-concurrency | static_heuristic | memory_barrier_present, barrier_between_data_and_index_update |
| `isr-concurrency-011` | isr-concurrency | static_heuristic | stack_overflow_protection_configured |
| `isr-concurrency-011` | isr-concurrency | static_heuristic | stack_overflow_protection_configured |
| `isr-concurrency-011` | isr-concurrency | static_heuristic | stack_overflow_protection_configured, isr_signals_via_semaphore |
| `isr-concurrency-012` | isr-concurrency | static_analysis | no_isr_unsafe_primitives |
| `isr-concurrency-012` | isr-concurrency | static_analysis | no_isr_unsafe_primitives |
| `kconfig-001` | kconfig | static_analysis | spi_dma_enabled |
| `kconfig-002` | kconfig | static_analysis | bt_hci_enabled |
| `kconfig-003` | kconfig | static_analysis | uart_line_ctrl_enabled |
| `kconfig-003` | kconfig | static_analysis | uart_line_ctrl_enabled |
| `kconfig-003` | kconfig | static_analysis | uart_line_ctrl_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_sockopt_tls_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_sockopt_tls_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_sockopt_tls_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_sockopt_tls_enabled |
| `kconfig-005` | kconfig | static_analysis | net_sockets_sockopt_tls_enabled, mbedtls_enabled |
| `memory-opt-001` | memory-opt | static_heuristic | block_size_defined |
| `memory-opt-001` | memory-opt | static_analysis | mem_slab_defined, slab_alloc_called, slab_free_called |
| `memory-opt-001` | memory-opt | static_heuristic | block_size_defined |
| `memory-opt-001` | memory-opt | static_heuristic | block_size_defined |
| `memory-opt-001` | memory-opt | static_heuristic | block_size_defined |
| `memory-opt-002` | memory-opt | static_analysis | isr_stack_size_defined |
| `memory-opt-002` | memory-opt | static_analysis | isr_stack_size_defined |
| `memory-opt-002` | memory-opt | static_analysis | heap_pool_size_set |
| `memory-opt-002` | memory-opt | static_heuristic | main_stack_size_reasonable, isr_stack_size_reasonable |
| `memory-opt-003` | memory-opt | static_analysis | heap_defined, heap_alloc_called, heap_free_called |
| `memory-opt-003` | memory-opt | static_analysis | heap_defined, heap_alloc_called, heap_free_called |
| `memory-opt-004` | memory-opt | static_heuristic | thread_analyzer_printk_backend |
| `memory-opt-004` | memory-opt | static_analysis | thread_stack_defined, thread_created |
| `memory-opt-005` | memory-opt | static_analysis | app_memdomain_header, partition_defined, thread_added_to_domain |
| `memory-opt-005` | memory-opt | static_analysis | app_memdomain_header, partition_defined |
| `memory-opt-005` | memory-opt | static_analysis | app_memdomain_header, partition_defined, thread_added_to_domain |
| `memory-opt-005` | memory-opt | static_analysis | app_memdomain_header, partition_defined |
| `memory-opt-005` | memory-opt | static_analysis | partition_defined |
| `memory-opt-006` | memory-opt | static_analysis | config_thread_stack_info_enabled |
| `memory-opt-006` | memory-opt | static_analysis | config_thread_stack_info_enabled |
| `memory-opt-006` | memory-opt | static_analysis | config_thread_stack_info_enabled |
| `memory-opt-008` | memory-opt | static_analysis | cbprintf_nano_enabled, dynamic_thread_disabled |
| `memory-opt-008` | memory-opt | static_analysis | cbprintf_nano_enabled, dynamic_thread_disabled |
| `memory-opt-008` | memory-opt | static_analysis | cbprintf_nano_enabled, dynamic_thread_disabled |
| `memory-opt-008` | memory-opt | static_analysis | cbprintf_nano_enabled, dynamic_thread_disabled |
| `memory-opt-008` | memory-opt | static_analysis | dynamic_thread_disabled |
| `memory-opt-012` | memory-opt | static_heuristic | no_large_string_literals |
| `memory-opt-012` | memory-opt | static_heuristic | no_large_string_literals |
| `memory-opt-012` | memory-opt | static_heuristic | no_large_string_literals |
| `memory-opt-012` | memory-opt | static_analysis | no_lookup_table |
| `networking-004` | networking | static_analysis | coap_packet_init_called, coap_append_option_called, uri_path_option, coap_get_method, coap_packet_parse_called, coap_header_get_code_called |
| `networking-006` | networking | static_heuristic | connection_closed_check |
| `networking-006` | networking | static_heuristic | connection_closed_check |
| `networking-006` | networking | static_heuristic | connection_closed_check |
| `networking-007` | networking | static_heuristic | timeout_not_infinite |
| `networking-007` | networking | static_heuristic | timeout_not_infinite |
| `networking-007` | networking | static_heuristic | timeout_not_infinite |
| `networking-007` | networking | static_heuristic | timeout_not_infinite |
| `networking-008` | networking | static_heuristic | connect_error_handling |
| `networking-008` | networking | static_heuristic | connect_error_handling |
| `networking-008` | networking | static_heuristic | connect_error_handling |
| `networking-008` | networking | static_heuristic | connect_error_handling |
| `ota-003` | ota | static_heuristic | done_after_write |
| `ota-003` | ota | static_heuristic | done_after_write |
| `ota-003` | ota | static_heuristic | done_after_write |
| `ota-003` | ota | static_heuristic | done_after_write |
| `ota-005` | ota | static_heuristic | rollback_abort_on_download_error, rollback_on_error |
| `ota-005` | ota | static_heuristic | rollback_abort_on_download_error, rollback_on_error |
| `ota-006` | ota | static_heuristic | dfu_done_false_on_mismatch |
| `ota-011` | ota | static_heuristic | self_test_failure_branch |
| `ota-011` | ota | static_heuristic | self_test_failure_branch |
| `ota-011` | ota | static_heuristic | self_test_failure_branch |
| `ota-011` | ota | static_heuristic | self_test_failure_branch |
| `ota-011` | ota | static_heuristic | self_test_failure_branch |
| `power-mgmt-001` | power-mgmt | static_heuristic | pm_error_handling |
| `power-mgmt-001` | power-mgmt | static_heuristic | pm_error_handling |
| `power-mgmt-002` | power-mgmt | static_heuristic | multiple_printk_calls |
| `power-mgmt-004` | power-mgmt | static_heuristic | enable_before_get |
| `power-mgmt-005` | power-mgmt | static_heuristic | all_three_devices_suspended, state_checked_before_resume |
| `power-mgmt-006` | power-mgmt | static_heuristic | pm_action_return_checked |
| `power-mgmt-006` | power-mgmt | static_heuristic | pm_action_return_checked |
| `security-002` | security | static_heuristic | hash_length_captured |
| `security-004` | security | static_heuristic | abort_in_error_paths |
| `security-005` | security | static_heuristic | data_verified_after_get |
| `security-007` | security | static_heuristic | error_path_returns_early |
| `security-007` | security | static_analysis | three_credentials_loaded, ca_certificate_type, private_key_type, return_value_checked |
| `security-008` | security | static_heuristic | mac_abort_in_error_paths |
| `security-008` | security | static_heuristic | error_path_key_destroyed, mac_abort_in_error_paths |
| `security-008` | security | static_heuristic | mac_abort_in_error_paths |
| `sensor-driver-003` | sensor-driver | static_heuristic | error_handling |
| `sensor-driver-006` | sensor-driver | static_analysis | sensor_device_dt_inst_define |
| `spi-i2c-001` | spi-i2c | static_heuristic | ready_check_before_io |
| `spi-i2c-004` | spi-i2c | static_heuristic | write_enable_before_write, poll_loop_bounded |
| `storage-001` | storage | static_heuristic | nvs_id_defined |
| `storage-002` | storage | static_heuristic | settings_handler_defined |
| `storage-002` | storage | static_heuristic | register_before_load, save_before_load |
| `storage-005` | storage | static_heuristic | mount_before_io |
| `storage-008` | storage | static_heuristic | write_verify_commit_order, delete_after_commit |
| `storage-008` | storage | static_heuristic | write_verify_commit_order, verify_before_commit, delete_after_commit |
| `storage-008` | storage | static_heuristic | write_verify_commit_order, verify_before_commit |
| `storage-008` | storage | static_heuristic | write_verify_commit_order, verify_before_commit, delete_after_commit |
| `storage-012` | storage | static_analysis | no_stdio_h |
| `storage-012` | storage | static_heuristic | write_rate_limited |
| `storage-012` | storage | static_heuristic | nvs_full_handling |
| `storage-012` | storage | static_analysis | no_stdio_h |
| `storage-012` | storage | static_heuristic | write_rate_limited |
| `storage-013` | storage | static_heuristic | handler_registered |
| `storage-013` | storage | static_analysis | settings_save_one_used |
| `storage-013` | storage | static_analysis | settings_save_one_used |
| `storage-013` | storage | static_analysis | save_not_unconditional_in_loop |
| `threading-001` | threading | static_heuristic | different_thread_priorities, queue_capacity_positive |
| `threading-001` | threading | static_heuristic | different_thread_priorities, queue_capacity_positive |
| `threading-001` | threading | static_heuristic | different_thread_priorities |
| `threading-006` | threading | static_heuristic | lock_order_a_before_b, unlock_order_b_before_a |
| `threading-007` | threading | static_heuristic | volatile_on_initialized_flag |
| `threading-007` | threading | static_heuristic | volatile_on_initialized_flag |
| `threading-007` | threading | static_heuristic | volatile_on_initialized_flag |
| `threading-007` | threading | static_heuristic | volatile_on_initialized_flag |
| `threading-008` | threading | static_heuristic | deadline_constant_not_magic |
| `threading-008` | threading | static_heuristic | deadline_constant_not_magic |
| `threading-008` | threading | static_heuristic | deadline_constant_not_magic |
| `threading-011` | threading | static_heuristic | high_priority_thread |
| `threading-011` | threading | static_heuristic | deadline_miss_detected, deadline_miss_action |
| `threading-011` | threading | static_heuristic | deadline_miss_action |
| `threading-011` | threading | static_heuristic | deadline_miss_detected, deadline_miss_action, high_priority_thread |
| `threading-011` | threading | static_heuristic | deadline_miss_detected, deadline_miss_action |
| `threading-012` | threading | static_heuristic | inter_thread_communication, priority_differentiation, uart_output_1s_interval, no_blocking_io_in_sensor |
| `threading-012` | threading | static_heuristic | priority_differentiation, uart_output_1s_interval, no_blocking_io_in_sensor |
| `threading-012` | threading | static_heuristic | inter_thread_communication, priority_differentiation, circular_buffer_filter, uart_output_1s_interval |
| `threading-012` | threading | static_heuristic | inter_thread_communication, priority_differentiation |
| `threading-012` | threading | static_heuristic | inter_thread_communication, circular_buffer_filter, uart_output_1s_interval, no_blocking_io_in_sensor |
| `threading-013` | threading | static_heuristic | handshake_mechanism, flag_cleared_after_read, data_before_flag |
| `threading-013` | threading | static_heuristic | handshake_mechanism, flag_cleared_after_read, data_before_flag |
| `threading-013` | threading | static_heuristic | volatile_on_shared_flags, handshake_mechanism, flag_cleared_after_read, data_before_flag, memory_barrier_present |
| `threading-013` | threading | static_heuristic | handshake_mechanism, flag_cleared_after_read, data_before_flag |
| `threading-013` | threading | static_heuristic | handshake_mechanism, flag_cleared_after_read, data_before_flag |
| `threading-014` | threading | static_analysis | explicit_memory_barrier, shared_flag_volatile, consumer_waits_for_flag |
| `threading-014` | threading | static_analysis | explicit_memory_barrier, shared_flag_volatile, consumer_waits_for_flag |
| `threading-014` | threading | static_analysis | explicit_memory_barrier |
| `threading-014` | threading | static_analysis | explicit_memory_barrier, shared_flag_volatile, consumer_waits_for_flag |
| `threading-014` | threading | static_analysis | explicit_memory_barrier, shared_flag_volatile, consumer_waits_for_flag |
| `timer-001` | timer | static_heuristic | counter_is_volatile |
| `timer-001` | timer | static_heuristic | counter_is_volatile |
| `timer-001` | timer | static_heuristic | counter_is_volatile |
| `timer-004` | timer | static_heuristic | worker_function_signature |
| `timer-004` | timer | static_heuristic | main_waits_for_work |
| `uart-002` | uart | static_heuristic | callback_before_rx_enable |
| `watchdog-001` | watchdog | static_heuristic | reset_soc_flag |
| `watchdog-001` | watchdog | static_heuristic | reset_soc_flag |
| `watchdog-001` | watchdog | static_heuristic | reset_soc_flag |
| `watchdog-002` | watchdog | static_heuristic | channel_id_stored |
| `watchdog-004` | watchdog | static_heuristic | install_before_setup |
| `watchdog-004` | watchdog | static_analysis | watchdog_header_included |
| `watchdog-004` | watchdog | static_heuristic | distinct_channel_timeouts, channel_ids_stored_separately |
| `watchdog-006` | watchdog | static_analysis | kernel_header_included |
| `watchdog-006` | watchdog | static_analysis | wdt_install_and_setup, reset_soc_flag |
| `watchdog-007` | watchdog | static_heuristic | all_threads_set_flags |
| `watchdog-010` | watchdog | static_heuristic | nvs_read_before_watchdog_setup |

## Failure Patterns

| Check Name | Failures | Cases |
|-----------|----------|-------|
| `dma_header_included` | 17 | dma-001, dma-002, dma-002, dma-002, dma-003 (+12 more) |
| `no_forbidden_apis_in_isr` | 6 | isr-concurrency-002, isr-concurrency-002, isr-concurrency-002, isr-concurrency-002, isr-concurrency-006 (+1 more) |
| `sample_buffer_nonzero` | 5 | adc-002, adc-002, adc-002, adc-002, adc-002 |
| `auth_state_reset_on_disconnect` | 5 | ble-006, ble-006, ble-006, ble-006, ble-006 |
| `cyclic_flag_set` | 5 | dma-003, dma-003, dma-003, dma-003, dma-003 |
| `multiple_block_descriptors` | 5 | dma-004, dma-004, dma-004, dma-004, dma-004 |
| `three_block_configs` | 5 | dma-011, dma-011, dma-011, dma-011, dma-011 |
| `net_sockets_sockopt_tls_enabled` | 5 | kconfig-005, kconfig-005, kconfig-005, kconfig-005, kconfig-005 |
| `partition_defined` | 5 | memory-opt-005, memory-opt-005, memory-opt-005, memory-opt-005, memory-opt-005 |
| `dynamic_thread_disabled` | 5 | memory-opt-008, memory-opt-008, memory-opt-008, memory-opt-008, memory-opt-008 |
| `self_test_failure_branch` | 5 | ota-011, ota-011, ota-011, ota-011, ota-011 |
| `handshake_mechanism` | 5 | threading-013, threading-013, threading-013, threading-013, threading-013 |
| `flag_cleared_after_read` | 5 | threading-013, threading-013, threading-013, threading-013, threading-013 |
| `data_before_flag` | 5 | threading-013, threading-013, threading-013, threading-013, threading-013 |
| `explicit_memory_barrier` | 5 | threading-014, threading-014, threading-014, threading-014, threading-014 |
| `interrupt_gpio_present` | 4 | device-tree-001, device-tree-001, device-tree-001, device-tree-001 |
| `pwm_polarity_specified` | 4 | device-tree-003, device-tree-003, device-tree-003, device-tree-003 |
| `dma_reload_called` | 4 | dma-003, dma-003, dma-003, dma-003 |
| `error_flag_is_volatile` | 4 | dma-008, dma-008, dma-008, dma-008 |
| `callback_sets_flag_on_error_status` | 4 | dma-008, dma-008, dma-008, dma-008 |
| `error_flag_causes_return` | 4 | dma-008, dma-008, dma-008, dma-008 |
| `error_flag_read_after_sync` | 4 | dma-008, dma-008, dma-008, dma-008 |
| `memory_barrier_present` | 4 | isr-concurrency-008, isr-concurrency-008, isr-concurrency-008, threading-013 |
| `block_size_defined` | 4 | memory-opt-001, memory-opt-001, memory-opt-001, memory-opt-001 |
| `app_memdomain_header` | 4 | memory-opt-005, memory-opt-005, memory-opt-005, memory-opt-005 |
| `cbprintf_nano_enabled` | 4 | memory-opt-008, memory-opt-008, memory-opt-008, memory-opt-008 |
| `timeout_not_infinite` | 4 | networking-007, networking-007, networking-007, networking-007 |
| `connect_error_handling` | 4 | networking-008, networking-008, networking-008, networking-008 |
| `done_after_write` | 4 | ota-003, ota-003, ota-003, ota-003 |
| `write_verify_commit_order` | 4 | storage-008, storage-008, storage-008, storage-008 |
| `volatile_on_initialized_flag` | 4 | threading-007, threading-007, threading-007, threading-007 |
| `deadline_miss_action` | 4 | threading-011, threading-011, threading-011, threading-011 |
| `inter_thread_communication` | 4 | threading-012, threading-012, threading-012, threading-012 |
| `priority_differentiation` | 4 | threading-012, threading-012, threading-012, threading-012 |
| `uart_output_1s_interval` | 4 | threading-012, threading-012, threading-012, threading-012 |
| `shared_flag_volatile` | 4 | threading-014, threading-014, threading-014, threading-014 |
| `consumer_waits_for_flag` | 4 | threading-014, threading-014, threading-014, threading-014 |
| `reset_soc_flag` | 4 | watchdog-001, watchdog-001, watchdog-001, watchdog-006 |
| `channel_priority_field_used` | 3 | dma-007, dma-007, dma-007 |
| `dma_start_called_twice` | 3 | dma-009, dma-009, dma-009 |
| `blocks_linked` | 3 | dma-011, dma-011, dma-011 |
| `init_before_isr_call` | 3 | isr-concurrency-005, isr-concurrency-005, isr-concurrency-005 |
| `barrier_between_data_and_index_update` | 3 | isr-concurrency-008, isr-concurrency-008, isr-concurrency-008 |
| `stack_overflow_protection_configured` | 3 | isr-concurrency-011, isr-concurrency-011, isr-concurrency-011 |
| `uart_line_ctrl_enabled` | 3 | kconfig-003, kconfig-003, kconfig-003 |
| `config_thread_stack_info_enabled` | 3 | memory-opt-006, memory-opt-006, memory-opt-006 |
| `no_large_string_literals` | 3 | memory-opt-012, memory-opt-012, memory-opt-012 |
| `connection_closed_check` | 3 | networking-006, networking-006, networking-006 |
| `mac_abort_in_error_paths` | 3 | security-008, security-008, security-008 |
| `delete_after_commit` | 3 | storage-008, storage-008, storage-008 |
| `verify_before_commit` | 3 | storage-008, storage-008, storage-008 |
| `different_thread_priorities` | 3 | threading-001, threading-001, threading-001 |
| `deadline_constant_not_magic` | 3 | threading-008, threading-008, threading-008 |
| `deadline_miss_detected` | 3 | threading-011, threading-011, threading-011 |
| `no_blocking_io_in_sensor` | 3 | threading-012, threading-012, threading-012 |
| `counter_is_volatile` | 3 | timer-001, timer-001, timer-001 |
| `bt_enable_before_scan` | 2 | ble-008, ble-008 |
| `conn_cleanup_on_failed_connect` | 2 | ble-008, ble-008 |
| `peripheral_to_memory_direction` | 2 | dma-002, dma-002 |
| `next_block_pointer_used` | 2 | dma-004, dma-004 |
| `error_flag_checked_after_wait` | 2 | dma-008, dma-008 |
| `dma_config_after_stop` | 2 | dma-009, dma-009 |
| `cache_flush_before_dma` | 2 | dma-012, dma-012 |
| `work_handler_does_processing` | 2 | isr-concurrency-005, isr-concurrency-005 |
| `fifo_reserved_field` | 2 | isr-concurrency-006, isr-concurrency-006 |
| `no_isr_unsafe_primitives` | 2 | isr-concurrency-012, isr-concurrency-012 |
| `isr_stack_size_defined` | 2 | memory-opt-002, memory-opt-002 |
| `heap_defined` | 2 | memory-opt-003, memory-opt-003 |
| `heap_alloc_called` | 2 | memory-opt-003, memory-opt-003 |
| `heap_free_called` | 2 | memory-opt-003, memory-opt-003 |
| `thread_added_to_domain` | 2 | memory-opt-005, memory-opt-005 |
| `rollback_abort_on_download_error` | 2 | ota-005, ota-005 |
| `rollback_on_error` | 2 | ota-005, ota-005 |
| `pm_error_handling` | 2 | power-mgmt-001, power-mgmt-001 |
| `pm_action_return_checked` | 2 | power-mgmt-006, power-mgmt-006 |
| `no_stdio_h` | 2 | storage-012, storage-012 |
| `write_rate_limited` | 2 | storage-012, storage-012 |
| `settings_save_one_used` | 2 | storage-013, storage-013 |
| `queue_capacity_positive` | 2 | threading-001, threading-001 |
| `high_priority_thread` | 2 | threading-011, threading-011 |
| `circular_buffer_filter` | 2 | threading-012, threading-012 |
| `auth_cb_before_advertising` | 1 | ble-005 |
| `security_set_in_connected_cb` | 1 | ble-006 |
| `discovery_after_connected` | 1 | ble-008 |
| `img_manager_dependency` | 1 | boot-001 |
| `two_gpio_pins_configured` | 1 | device-tree-005 |
| `source_addr_fixed` | 1 | dma-002 |
| `dest_addr_increments` | 1 | dma-002 |
| `dma_start_called` | 1 | dma-002 |
| `config_before_start` | 1 | dma-005 |
| `aligned_attribute_present` | 1 | dma-006 |
| `two_dma_config_calls` | 1 | dma-007 |
| `two_dma_start_calls` | 1 | dma-007 |
| `timeout_mechanism_present` | 1 | dma-009 |
| `block_count_three` | 1 | dma-011 |
| `head_block_set` | 1 | dma-011 |
| `device_ready_check` | 1 | dma-012 |
| `wait_for_completion` | 1 | dma-012 |
| `direction_memory_to_memory` | 1 | dma-012 |
| `no_printk` | 1 | isr-concurrency-001 |
| `zephyr_headers_included` | 1 | isr-concurrency-001 |
| `no_printk_in_isr` | 1 | isr-concurrency-002 |
| `consumer_uses_k_forever` | 1 | isr-concurrency-002 |
| `message_struct_defined` | 1 | isr-concurrency-002 |
| `k_work_declared` | 1 | isr-concurrency-005 |
| `k_work_init_called` | 1 | isr-concurrency-005 |
| `k_work_submit_called` | 1 | isr-concurrency-005 |
| `work_handler_correct_signature` | 1 | isr-concurrency-005 |
| `k_fifo_get_not_in_isr` | 1 | isr-concurrency-006 |
| `high_priority_lower_number` | 1 | isr-concurrency-007 |
| `isr_signals_via_semaphore` | 1 | isr-concurrency-011 |
| `spi_dma_enabled` | 1 | kconfig-001 |
| `bt_hci_enabled` | 1 | kconfig-002 |
| `mbedtls_enabled` | 1 | kconfig-005 |
| `mem_slab_defined` | 1 | memory-opt-001 |
| `slab_alloc_called` | 1 | memory-opt-001 |
| `slab_free_called` | 1 | memory-opt-001 |
| `heap_pool_size_set` | 1 | memory-opt-002 |
| `main_stack_size_reasonable` | 1 | memory-opt-002 |
| `isr_stack_size_reasonable` | 1 | memory-opt-002 |
| `thread_analyzer_printk_backend` | 1 | memory-opt-004 |
| `thread_stack_defined` | 1 | memory-opt-004 |
| `thread_created` | 1 | memory-opt-004 |
| `no_lookup_table` | 1 | memory-opt-012 |
| `coap_packet_init_called` | 1 | networking-004 |
| `coap_append_option_called` | 1 | networking-004 |
| `uri_path_option` | 1 | networking-004 |
| `coap_get_method` | 1 | networking-004 |
| `coap_packet_parse_called` | 1 | networking-004 |
| `coap_header_get_code_called` | 1 | networking-004 |
| `dfu_done_false_on_mismatch` | 1 | ota-006 |
| `multiple_printk_calls` | 1 | power-mgmt-002 |
| `enable_before_get` | 1 | power-mgmt-004 |
| `all_three_devices_suspended` | 1 | power-mgmt-005 |
| `state_checked_before_resume` | 1 | power-mgmt-005 |
| `hash_length_captured` | 1 | security-002 |
| `abort_in_error_paths` | 1 | security-004 |
| `data_verified_after_get` | 1 | security-005 |
| `error_path_returns_early` | 1 | security-007 |
| `three_credentials_loaded` | 1 | security-007 |
| `ca_certificate_type` | 1 | security-007 |
| `private_key_type` | 1 | security-007 |
| `return_value_checked` | 1 | security-007 |
| `error_path_key_destroyed` | 1 | security-008 |
| `error_handling` | 1 | sensor-driver-003 |
| `sensor_device_dt_inst_define` | 1 | sensor-driver-006 |
| `ready_check_before_io` | 1 | spi-i2c-001 |
| `write_enable_before_write` | 1 | spi-i2c-004 |
| `poll_loop_bounded` | 1 | spi-i2c-004 |
| `nvs_id_defined` | 1 | storage-001 |
| `settings_handler_defined` | 1 | storage-002 |
| `register_before_load` | 1 | storage-002 |
| `save_before_load` | 1 | storage-002 |
| `mount_before_io` | 1 | storage-005 |
| `nvs_full_handling` | 1 | storage-012 |
| `handler_registered` | 1 | storage-013 |
| `save_not_unconditional_in_loop` | 1 | storage-013 |
| `lock_order_a_before_b` | 1 | threading-006 |
| `unlock_order_b_before_a` | 1 | threading-006 |
| `volatile_on_shared_flags` | 1 | threading-013 |
| `worker_function_signature` | 1 | timer-004 |
| `main_waits_for_work` | 1 | timer-004 |
| `callback_before_rx_enable` | 1 | uart-002 |
| `channel_id_stored` | 1 | watchdog-002 |
| `install_before_setup` | 1 | watchdog-004 |
| `watchdog_header_included` | 1 | watchdog-004 |
| `distinct_channel_timeouts` | 1 | watchdog-004 |
| `channel_ids_stored_separately` | 1 | watchdog-004 |
| `kernel_header_included` | 1 | watchdog-006 |
| `wdt_install_and_setup` | 1 | watchdog-006 |
| `all_threads_set_flags` | 1 | watchdog-007 |
| `nvs_read_before_watchdog_setup` | 1 | watchdog-010 |

## TC Improvement Suggestions

