import itertools
import pytest

import forta_toolkit.parsing.common as fpc
import forta_toolkit.parsing.traces as fpt
import tests.test_data as td

# FIXTURES ####################################################################

@pytest.fixture
def __data():
    return [fpt.parse_trace_data(__t) for __traces in td.ALL_TRACES for __t in __traces]

@pytest.fixture
def trace_keys() -> set:
    return {'chain_id', 'block_hash', 'block_number', 'transaction_hash', 'transaction_index', 'error', 'subtraces', 'trace_address', 'action_type', 'action_call_type', 'action_reward_type', 'action_gas', 'action_from', 'action_to', 'action_input', 'action_init', 'action_value', 'result_address', 'result_gas_used', 'result_code', 'result_output'}

# FORMAT ######################################################################

def test_trace_data_has_a_fixed_structure_after_parsing(__data, trace_keys):
    assert all([type(__d) == dict for __d in __data])
    assert all([type(__v) == str or type(__v) == list for __d in __data for __v in __d.values()])
    assert all([set(__d.keys()) == trace_keys for __d in __data])

# CONTENT #####################################################################

def test_trace_data_fields_are_all_filled_after_parsing(__data):
    # always filled
    assert all([len(__d.get('block_number', '')) for __d in __data])
    assert all([len(__d.get('transaction_hash', '')) for __d in __data])
    assert all([len(__d.get('action_type', '')) for __d in __data])
    # can be empty, but not always
    assert any([len(__d.get('action_gas', '')) for __d in __data])
    assert any([len(__d.get('action_from', '')) for __d in __data])
    assert any([len(__d.get('action_to', '')) for __d in __data])
    assert any([len(__d.get('action_input', '')) for __d in __data])
    assert any([len(__d.get('action_init', '')) for __d in __data])
    assert any([len(__d.get('action_value', '')) for __d in __data])
    assert any([len(__d.get('result_address', '')) for __d in __data])
    assert any([len(__d.get('result_gas_used', '')) for __d in __data])
    assert any([len(__d.get('result_code', '')) for __d in __data])
    assert any([len(__d.get('result_output', '')) for __d in __data])

def test_trace_data_fields_have_consistent_values_after_parsing(__data):
    # HEX encoded strings
    assert all([fpc.is_hexstr(__d.get('block_number', '')) for __d in __data])
    assert all([fpc.is_hexstr(__d.get('transaction_hash', '')) for __d in __data])
    assert all([fpc.is_hexstr(__d.get('action_from', '')) for __d in __data])
    assert any([fpc.is_hexstr(__d.get('action_gas', '')) for __d in __data])
    assert any([fpc.is_hexstr(__d.get('action_to', '')) for __d in __data])
    assert any([fpc.is_hexstr(__d.get('action_input', '')) for __d in __data])
    assert any([fpc.is_hexstr(__d.get('action_init', '')) for __d in __data])
    assert any([fpc.is_hexstr(__d.get('action_value', '')) for __d in __data])
    assert any([fpc.is_hexstr(__d.get('result_address', '')) for __d in __data])
    assert any([fpc.is_hexstr(__d.get('result_gas_used', '')) for __d in __data])
    assert any([fpc.is_hexstr(__d.get('result_code', '')) for __d in __data])
    assert any([fpc.is_hexstr(__d.get('result_output', '')) for __d in __data])
    # categorical data
    assert all([__d.get('action_type', '') in ('call', 'create', 'suicide', 'delegatecall', 'callcode', 'staticcall') for __d in __data])

# ITERATION ###################################################################

def test_parsing_already_parsed_data_leaves_it_unchanged(__data):
    assert all([fpt.parse_trace_data(__t) == __t for __t in __data])
