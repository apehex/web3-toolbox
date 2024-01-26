import itertools
import pytest

import toolblocks.parsing.common as fpc
import toolblocks.parsing.transaction as fpt
import tests.test_data as td

# FIXTURES ####################################################################

@pytest.fixture
def __data() -> list:
    return [fpt.parse_transaction_data(__t) for __t in td.ALL_TRANSACTIONS]

@pytest.fixture
def transaction_keys() -> set:
    return {'chain_id', 'block_number', 'transaction_hash', 'transaction_type', 'transaction_index', 'nonce', 'gas_used', 'gas_limit', 'gas_price', 'max_fee_per_gas', 'max_priority_fee_per_gas', 'success', 'from_address', 'to_address', 'value', 'input'}

# FORMAT ######################################################################

def test_transaction_data_has_a_fixed_structure_after_parsing(__data, transaction_keys):
    assert all([type(__d) == dict for __d in __data])
    assert all([type(__v) == str for __d in __data for __v in __d.values()])
    assert all([set(__d.keys()) == transaction_keys for __d in __data])

# CONTENT #####################################################################

def test_transaction_data_fields_are_all_filled_after_parsing(__data):
    # always filled
    assert all([len(__d.get('transaction_hash', '')) for __d in __data])
    assert all([len(__d.get('nonce', '')) for __d in __data])
    assert all([len(__d.get('gas_used', '')) for __d in __data])
    assert all([len(__d.get('gas_price', '')) for __d in __data])
    assert all([len(__d.get('from_address', '')) for __d in __data])
    # can be empty, but not always
    assert any([len(__d.get('to_address', '')) for __d in __data])
    assert any([len(__d.get('input', '')) for __d in __data])
    assert any([len(__d.get('value', '')) for __d in __data])

def test_transaction_data_fields_have_consistent_values_after_parsing(__data):
    # always filled
    assert all([fpc.is_hexstr(__d.get('transaction_hash', '')) for __d in __data])
    assert all([fpc.is_hexstr(__d.get('nonce', '')) for __d in __data])
    assert all([fpc.is_hexstr(__d.get('gas_used', '')) for __d in __data])
    assert all([fpc.is_hexstr(__d.get('gas_price', '')) for __d in __data])
    assert all([fpc.is_hexstr(__d.get('from_address', '')) for __d in __data])
    # can be empty, but not always
    assert all([fpc.is_hexstr(__d.get('to_address', '')) for __d in __data])
    assert all([fpc.is_hexstr(__d.get('input', '')) for __d in __data])
    assert all([fpc.is_hexstr(__d.get('value', '')) for __d in __data])

# ITERATION ###################################################################

def test_parsing_already_parsed_data_leaves_it_unchanged(__data):
    assert all([fpt.parse_transaction_data(__t) == __t for __t in __data])

