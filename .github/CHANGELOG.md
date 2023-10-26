# Changelog

## v0.1.11 - v0.1.13

### Changes

- parse both Forta and std RPC formats for the traces (`transaction_hash` vs `transactionHash`)
- sanitize and format all the data as HEX strings

## v0.1.10

### Changes

- renamed `forta_toolkit/parsing/logs.py` to `forta_toolkit/parsing/transaction.py`

### Additions

- reformat and flatten transaction traces
