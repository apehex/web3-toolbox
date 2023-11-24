import itertools
import pytest

import forta_toolkit.parsing.common as fpc
import forta_toolkit.parsing.traces as fpt
import tests.test_data as td

# FIXTURES ####################################################################

@pytest.fixture
def __data():
    return [fpt.parse_trace_data(__t) for __traces in td.ALL_TRACES for __t in __traces]

# FORMAT ######################################################################

def test_trace_data_has_a_fixed_structure_after_parsing(__data):
    assert all([type(__d) == dict for __d in __data])
    assert all([type(__v) == str or type(__v) == int for __d in __data for __v in __d.values()])
    assert all([set(__d.keys()) == {'block', 'hash', 'type', 'value', 'gas', 'from', 'to', 'input', 'output'} for __d in __data])

# CONTENT #####################################################################

def test_trace_data_fields_are_all_filled_after_parsing(__data):
    # always filled
    assert all([len(__d.get('block', '')) for __d in __data])
    assert all([len(__d.get('hash', '')) for __d in __data])
    assert all([len(__d.get('type', '')) for __d in __data])
    assert all([len(__d.get('from', '')) for __d in __data])
    # can be empty, but not always
    assert any([len(__d.get('value', '')) for __d in __data])
    assert any([len(__d.get('gas', '')) for __d in __data])
    assert any([len(__d.get('to', '')) for __d in __data])
    assert any([len(__d.get('input', '')) for __d in __data])
    assert any([len(__d.get('output', '')) for __d in __data])

def test_trace_data_fields_have_consistent_values_after_parsing(__data):
    # HEX encoded strings
    assert all([fpc.is_hexstr(__d.get('block', '')) for __d in __data])
    assert all([fpc.is_hexstr(__d.get('hash', '')) for __d in __data])
    assert all([fpc.is_hexstr(__d.get('from', '')) for __d in __data])
    assert all([not bool(__d.get('value', '')) or fpc.is_hexstr(__d.get('value', '')) for __d in __data])
    assert all([not bool(__d.get('gas', '')) or fpc.is_hexstr(__d.get('gas', '')) for __d in __data])
    assert all([not bool(__d.get('to', '')) or fpc.is_hexstr(__d.get('to', '')) for __d in __data])
    assert all([not bool(__d.get('input', '')) or fpc.is_hexstr(__d.get('input', '')) for __d in __data])
    assert all([not bool(__d.get('output', '')) or fpc.is_hexstr(__d.get('output', '')) for __d in __data])
    # categorical data
    assert all([__d.get('type', '') in ('call', 'create', 'suicide', 'delegatecall', 'callcode', 'staticcall') for __d in __data])

# ITERATION ###################################################################

def test_parsing_already_parsed_data_leaves_it_unchanged(__data):
    assert all([fpt.parse_trace_data(__t) == __t for __t in __data])
