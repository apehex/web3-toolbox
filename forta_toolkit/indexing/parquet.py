"""Save and index the bot data on the disk."""

import functools
import os
import typing

import eth_utils.crypto
import pyarrow.dataset
import pyarrow.lib

import forta_toolkit.parsing.common
import forta_toolkit.parsing.logs
import forta_toolkit.parsing.traces
import forta_toolkit.parsing.transaction

# CONSTANTS ###################################################################

PATH = '.data/parquet/{dataset}/'

# DATABASE SCHEMAS ############################################################

SCHEMAS = {

# TRANSACTIONS

    'transactions': pyarrow.schema([
        pyarrow.lib.field('chain_id', pyarrow.uint64()),
        pyarrow.lib.field('block_number', pyarrow.uint64()),
        pyarrow.lib.field('transaction_hash', pyarrow.binary()),
        pyarrow.lib.field('transaction_type', pyarrow.uint32()),
        pyarrow.lib.field('transaction_index', pyarrow.uint64()),
        pyarrow.lib.field('nonce', pyarrow.uint64()),
        pyarrow.lib.field('gas_used', pyarrow.uint64()),
        pyarrow.lib.field('gas_limit', pyarrow.uint64()),
        pyarrow.lib.field('gas_price', pyarrow.uint64()),
        pyarrow.lib.field('max_fee_per_gas', pyarrow.uint64()),
        pyarrow.lib.field('max_priority_fee_per_gas', pyarrow.uint64()),
        pyarrow.lib.field('success', pyarrow.bool_()),
        pyarrow.lib.field('from_address', pyarrow.binary()),
        pyarrow.lib.field('to_address', pyarrow.binary()),
        pyarrow.lib.field('value_binary', pyarrow.binary()),
        pyarrow.lib.field('value_string', pyarrow.string()),
        pyarrow.lib.field('value_f64', pyarrow.float64()),
        pyarrow.lib.field('input', pyarrow.binary()),]),

# LOGS

    'logs': pyarrow.schema([
        pyarrow.lib.field('chain_id', pyarrow.uint64()),
        pyarrow.lib.field('block_number', pyarrow.uint32()),
        pyarrow.lib.field('transaction_hash', pyarrow.binary()),
        pyarrow.lib.field('transaction_index', pyarrow.uint32()),
        pyarrow.lib.field('address', pyarrow.binary()),
        pyarrow.lib.field('log_index', pyarrow.uint32()),
        pyarrow.lib.field('topic0', pyarrow.binary()),
        pyarrow.lib.field('topic2', pyarrow.binary()),
        pyarrow.lib.field('topic1', pyarrow.binary()),
        pyarrow.lib.field('topic3', pyarrow.binary()),
        pyarrow.lib.field('data', pyarrow.binary()),]),

# TRACES

    'traces': pyarrow.schema([
        pyarrow.lib.field('chain_id', pyarrow.uint64()),
        pyarrow.lib.field('block_hash', pyarrow.binary()),
        pyarrow.lib.field('block_number', pyarrow.uint32()),
        pyarrow.lib.field('transaction_hash', pyarrow.binary()),
        pyarrow.lib.field('transaction_index', pyarrow.uint32()),
        pyarrow.lib.field('action_type', pyarrow.string()),
        pyarrow.lib.field('action_call_type', pyarrow.string()),
        pyarrow.lib.field('action_reward_type', pyarrow.string()),
        pyarrow.lib.field('action_gas', pyarrow.uint32()),
        pyarrow.lib.field('action_from', pyarrow.binary()),
        pyarrow.lib.field('action_to', pyarrow.binary()),
        pyarrow.lib.field('action_input', pyarrow.binary()),
        pyarrow.lib.field('action_init', pyarrow.binary()),
        pyarrow.lib.field('action_value', pyarrow.string()),
        pyarrow.lib.field('result_address', pyarrow.binary()),
        pyarrow.lib.field('result_gas_used', pyarrow.uint32()),
        pyarrow.lib.field('result_code', pyarrow.binary()),
        pyarrow.lib.field('result_output', pyarrow.binary()),
        pyarrow.lib.field('trace_address', pyarrow.string()),
        pyarrow.lib.field('subtraces', pyarrow.uint32()),
        pyarrow.lib.field('error', pyarrow.string()),]),

# CONTRACTS

    'contracts': pyarrow.schema([
        pyarrow.lib.field('chain_id', pyarrow.uint64()),
        pyarrow.lib.field('block_number', pyarrow.uint32()),
        pyarrow.lib.field('transaction_hash', pyarrow.binary()),
        pyarrow.lib.field('deployer', pyarrow.binary()),
        pyarrow.lib.field('contract_address', pyarrow.binary()),
        pyarrow.lib.field('create_index', pyarrow.uint32()),
        pyarrow.lib.field('init_code', pyarrow.binary()),
        pyarrow.lib.field('init_code_hash', pyarrow.binary()),
        pyarrow.lib.field('code', pyarrow.binary()),
        pyarrow.lib.field('code_hash', pyarrow.binary()),
        pyarrow.lib.field('factory', pyarrow.binary()),]),
}

# CASTING #####################################################################

def _list_contract_creations(traces: list, chain_id: int=1, schema: pyarrow.lib.Schema=SCHEMAS['contracts']) -> list:
    """List all the contracts that were created during a transaction."""
    __rows = []
    for __t in traces:
        if 'create' in __t.get('action_type', ''):
            __r = {__k: None for __k in schema.names}
            # hash the bytecode
            __creation_bytecode = forta_toolkit.parsing.common.to_bytes(__t.get('action_init', None))
            __creation_bytecode_hash = forta_toolkit.parsing.common.to_bytes(eth_utils.crypto.keccak(primitive=__creation_bytecode))
            __runtime_bytecode = forta_toolkit.parsing.common.to_bytes(__t.get('result_code', None))
            __runtime_bytecode_hash = forta_toolkit.parsing.common.to_bytes(eth_utils.crypto.keccak(primitive=__runtime_bytecode))
            # fill the fields
            __r['chain_id'] = chain_id
            __r['block_number'] = forta_toolkit.parsing.common.to_int(__t.get('block_number', None))
            __r['transaction_hash'] = forta_toolkit.parsing.common.to_bytes(__t.get('transaction_hash', None))
            __r['deployer'] = forta_toolkit.parsing.common.to_bytes(__t.get('action_from', None))
            __r['contract_address'] = forta_toolkit.parsing.common.to_bytes(__t.get('result_address', None))
            __r['create_index'] = None
            __r['init_code'] = __creation_bytecode
            __r['init_code_hash'] = __creation_bytecode_hash
            __r['code'] = __runtime_bytecode
            __r['code_hash'] = __runtime_bytecode_hash
            __r['factory'] = None
            # add to the list of contracts
            __rows.append(__r)
    return __rows

def _to_table(rows: list, schema: pyarrow.lib.Schema) -> pyarrow.Table:
    """Format a list of rows (dict) as a pyarrow table."""
    return pyarrow.lib.Table.from_pylist(mapping=rows, schema=schema)

# IMPORT ######################################################################

def import_from_database(chain_id: int=1, dataset: str='contracts', path: str=PATH) -> callable:
    """Creates a decorator for handle_transaction to add a connection to the database as argument."""
    # init
    __path = path.format(chain_id=chain_id, dataset=dataset)
    __schema = SCHEMAS.get(dataset, None)
    # create parent dir if it doesn't exist
    os.makedirs(name=__path, exist_ok=True)

    def __decorator(func: callable) -> callable:
        """Actually wraps the handle_transaction and saves items in the database."""

        @functools.wraps(func)
        def __wrapper(*args, **kwargs):
            """Main function called on the logs gathered by the Forta network."""
            # access factory arguments
            nonlocal __dataset
            # pass the argument, without forcing
            kwargs['dataset'] = __dataset
            # call handle_transaction
            return func(*args, **kwargs)

        return __wrapper

    return __decorator

# EXPORT ######################################################################

# TODO get relevant data from:
#   - TransactionEvent
#   - transaction, logs, traces

def _write_dataset(table: pyarrow.lib.Table, path: str, schema: pyarrow.lib.Schema, chunk: int=0) -> None:
    """Append a table to a dataset."""
    pyarrow.dataset.write_dataset(
        data=table,
        base_dir=path,
        basename_template="part-{chunk}-{{i}}.parquet".format(chunk=chunk),
        partitioning=['chain_id'],
        schema=schema,
        format='parquet',
        existing_data_behavior='overwrite_or_ignore')

def export_to_database(chain_id: int=1, dataset: str='contracts', path: str=PATH, chunksize: int=2**10) -> callable:
    """Creates a decorator for handle_transaction save and index all the data it handles."""
    # init
    __rows = []
    __path = path.format(chain_id=chain_id, dataset=dataset)
    # create parent dir
    os.makedirs(name=__path, exist_ok=True)
    # append to the existing batch
    __chunk = len(os.listdir(__path))

    def __decorator(func: callable) -> callable:
        """Actually wraps the handle_transaction and saves items in the database."""

        @functools.wraps(func)
        def __wrapper(*args, **kwargs):
            """Main function called on the logs gathered by the Forta network."""
            # access factory arguments
            nonlocal __chunk, __rows, __path
            # parse data
            __traces = kwargs.get('traces', [])
            # format the contract creations as database rows
            __rows.extend(_list_contract_creations(traces=__traces, chain_id=chain_id))
            # save to disk
            if len(__rows) >= chunksize:
                __table = _to_table(rows=__rows, schema=SCHEMAS['contracts'])
                _write_dataset(table=__table, path=__path, schema=SCHEMAS['contracts'], chunk=__chunk)
                __chunk += 1
                __rows = []
            # process the transaction
            __findings = func(*args, **kwargs)
            # return the findings
            return __findings

        return __wrapper

    return __decorator
