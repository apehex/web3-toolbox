# Changelog

## v0.1.19 - v0.1.22

### Changes

- remove the `forta_agent` and `web3` dependencies
- `parse_transaction_data`, `parse_log_data` and `parse_trace_data` all use `get_field`
- the parsing functions handle Forta objects, RPC results and simpler dictionaries to represent tx, logs, etc with `get_field`
- fix various edge cases

### Additions

- definitive functions for data sanitizing & formatting into common, consistent types
- tests for all the modules
- documentation for the features

## v0.1.18

### Changes

- remove the log of findings in `format_findings_factory`

### Additions

- parse, sanitize & flatten event logs

## v0.1.14 - v0.1.17

### Additions

- generic function to format detection data into a Forta alert object with labels

## v0.1.11 - v0.1.13

### Changes

- parse both Forta and std RPC formats for the traces (`transaction_hash` vs `transactionHash`)
- sanitize and format all the data as HEX strings

## v0.1.10

### Changes

- renamed `forta_toolkit/parsing/logs.py` to `forta_toolkit/parsing/transaction.py`

### Additions

- reformat and flatten transaction traces
