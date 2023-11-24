import itertools
import pytest

import forta_toolkit.parsing.common as fpc
import forta_toolkit.parsing.logs as fpl
import tests.test_data as td

# FIXTURES ####################################################################

@pytest.fixture
def __data():
    return [fpl.parse_log_data(__l) for __logs in td.ALL_LOGS for __l in __logs]

# PARSING #####################################################################

def test_log_data_has_a_fixed_structure_after_parsing(__data):
    assert all([type(__d) == dict for __d in __data])
    assert all([type(__v) == str or type(__v) == list for __d in __data for __v in __d.values()])
    assert all([set(__d.keys()).issuperset({'block', 'hash', 'index', 'address', 'topics', 'data'}) for __d in __data]) # contains key alias too, like "logIndex"

# CONTENT #####################################################################

def test_log_data_fields_are_all_filled_after_parsing(__data):
    # always filled
    assert all([len(__d.get('block', '')) for __d in __data])
    assert all([len(__d.get('hash', '')) for __d in __data])
    assert all([len(__d.get('index', '')) for __d in __data])
    assert all([len(__d.get('address', '')) for __d in __data])
    # can be empty, but not always
    assert any([len(__d.get('topics', '')) for __d in __data])
    assert any([len(__d.get('data', '')) for __d in __data])

def test_log_data_fields_have_consistent_values_after_parsing(__data):
    # HEX encoded strings
    assert all([fpc.is_hexstr(__d.get('block', '')) for __d in __data])
    assert all([fpc.is_hexstr(__d.get('hash', '')) for __d in __data])
    assert all([fpc.is_hexstr(__d.get('index', '')) for __d in __data])
    assert all([fpc.is_hexstr(__d.get('address', '')) for __d in __data])
    assert all([not bool(__d.get('data', '')) or fpc.is_hexstr(__d.get('data', '')) for __d in __data])
    # list
    assert all([isinstance(__d.get('topics', []), list) for __d in __data])

# ITERATION ###################################################################

def test_parsing_already_parsed_data_leaves_it_unchanged(__data):
    assert all([fpl.parse_log_data(__l) == __l for __l in __data])
