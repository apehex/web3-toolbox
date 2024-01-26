import itertools
import pytest

import toolblocks.parsing.common as fpc

# FIXTURES ####################################################################

class MixedAttributeDict(dict):
    def __init__(self):
        self.__setitem__('first', 1)
        self.second = 2

@pytest.fixture
def non_iterable_data():
    return [1234, -3.1, lambda x: x, None]

@pytest.fixture
def iterable_data():
    return ['1234', {}, (), [], b'deadbeef']

@pytest.fixture
def non_hexstr_data():
    return [1234, 'fgh', '0xdj']

@pytest.fixture
def hexstr_data():
    return ['1234', '0x2', '0x', '', '0xdeadbeef', 'AAAAAA', 'aaaaaa']

@pytest.fixture
def attribute_dict():
    return MixedAttributeDict()

# DATA IDENTIFICATION #########################################################

def test_is_iterable_on_random_data(non_iterable_data, iterable_data):
    __nope = [fpc.is_iterable(__d) for __d in non_iterable_data]
    __yeah = [fpc.is_iterable(__d) for __d in iterable_data]
    assert not any(__nope)
    assert all(__yeah)

def test_is_hexstr_on_random_data(non_hexstr_data, hexstr_data):
    __nope = [fpc.is_hexstr(__d) for __d in non_hexstr_data]
    __yeah = [fpc.is_hexstr(__d) for __d in hexstr_data]
    assert not any(__nope)
    assert all(__yeah)

# CONVERSIONS #################################################################

def test_normalized_hexstr_format(hexstr_data):
    __normalized = [fpc.normalize_hexstr(__d) for __d in hexstr_data]
    assert all([len(__d) % 2 == 0 for __d in __normalized])
    assert all([not __d.startswith('0x') for __d in __normalized])
    assert all([__d == __d.lower() for __d in __normalized])

def test_to_hexstr_always_returns_a_string(non_iterable_data, iterable_data, non_hexstr_data, hexstr_data):
    assert all([type(fpc.to_hexstr(__d)) == str for __d in itertools.chain(non_iterable_data, iterable_data, non_hexstr_data, hexstr_data)])

def test_normalization_keeps_normal_data_unchanged(hexstr_data):
    __normalized = [fpc.normalize_hexstr(__d) for __d in hexstr_data]
    assert all([__d == fpc.normalize_hexstr(__d) for __d in __normalized])

def test_conversions_from_target_types_leave_data_unchanged(non_iterable_data, iterable_data, non_hexstr_data, hexstr_data):
    __hexstr_data = [fpc.to_hexstr(__d) for __d in itertools.chain(non_iterable_data, iterable_data, non_hexstr_data, hexstr_data)]
    __bytes_data = [fpc.to_bytes(__d) for __d in itertools.chain(non_iterable_data, iterable_data, non_hexstr_data, hexstr_data)]
    __int_data = [fpc.to_int(__d) for __d in itertools.chain(non_iterable_data, iterable_data, non_hexstr_data, hexstr_data)]
    assert all([__d == fpc.to_hexstr(__d) for __d in __hexstr_data])
    assert all([__d == fpc.to_bytes(__d) for __d in __bytes_data])
    assert all([__d == fpc.to_int(__d) for __d in __int_data])

# ACCESS ######################################################################

def test_access_functions_work_both_on_standard_and_attribute_dict(attribute_dict):
    assert fpc.get_field_alias(dataset=attribute_dict, key='first', default='out') == 1
    assert fpc.get_field_alias(dataset=attribute_dict, key='second', default='out') == 2
    assert fpc.get_field_alias(dataset=attribute_dict, key=3, default='out') == 'out'
    assert fpc.get_field(dataset=attribute_dict, keys=('first', 1), default='out') == 1
    assert fpc.get_field(dataset=attribute_dict, keys=('second', 'b'), default='out') == 2
    assert fpc.get_field(dataset=attribute_dict, keys=('c', 3), default='out') == 'out'

def test_access_functions_always_call_the_callback(attribute_dict):
    assert fpc.get_field(dataset=attribute_dict, keys=('first',), default='out', callback=print) == None
    assert fpc.get_field(dataset=attribute_dict, keys=('b', 'second',), default='out', callback=str) == '2'
    assert fpc.get_field(dataset=attribute_dict, keys=('heyhey', 'blehbleh', -1), default='out', callback=len) == len('out')
