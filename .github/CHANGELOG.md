# Changelog

## v0.4.6

### Fixes

- fix IO path for parquet datasets

## v0.4.3 - v0.4.5

### Changes

- relax the depency version requirements to allow installation on older systems
- process transaction *before* commiting the data to disk
- refresh the datasets on each call of `handle_transaction`

### Additions

- add `compress` option to the parquet exportation to spare disk space
- query the contracts dataset and list past deployments at a given address

## v0.4.2

### Changes

- now requires the `pyarrow` and `eth-utils` dependencies

### Additions

- add `import_from_database` and `export_to_database` to manage the blockchain history; the schema is the same as [`cryo`][github-cryo] and it saves:
  - transactions
  - logs
  - traces
  - contracts
  - findings

## v0.4.1

### Changes

- split the `indexing` module by format: `forta_toolkit.indexing.pickle` and `forta_toolkit.indexing.parquet`
- changed the keys of the `transaction`, `logs` and `traces` to accomodate all the data from the nodes
- toggle the "0x" prefix on HEX strings (default: no prefix)
- the prefix is systematically prepended to the parsed data
- bot version must be passed to `setup_logger` explicitely
- consider "0x" and "" as valid empty HEX strings

## v0.3.2

### Changes

- move the module `forta_toolkit.indexing.dump` to `forta_toolkit.indexing`
- rename the function `serialize` in `forta_toolkit.indexing` to `serialize_io`

## v0.3.1

### Additions

- add the decorator `parse_forta_arguments` to split, parse the `TransactionEvent` into `transaction`, `logs` and `traces`
- also sanitize the input data and guarantee a fixed structure

## v0.2.1

### Fixes

- `parse_transaction_data`, `parse_log_data` and `parse_trace_data` now leave the data unchanged if it was already parsed

### Additions

- add the decorator `forta_toolkit.indexing.dump.serialize` to automatically pickle the IO of `handle_transaction`

## v0.1.23

### Fixes

- respect the order in which field aliases are queried when using `get` with a list of keys (left to right)

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

[github-cryo]: https://github.com/paradigmxyz/cryo
