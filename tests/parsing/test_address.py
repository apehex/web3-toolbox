import pytest

import forta_toolkit.parsing.address as fpa

# FIXTURES ####################################################################

@pytest.fixture
def empty_addresses():
    return ['', None, '0x']

@pytest.fixture
def incomplete_addresses():
    return [512, '9485f1', '0x1', False, 0] # null is different from empty

# FORMAT ######################################################################

def test_null_address_stays_empty_after_formatting(empty_addresses):
    __formatted = [fpa.format_with_checksum(__a) for __a in empty_addresses]
    assert all(__a == '' for __a in __formatted)

def test_address_format(incomplete_addresses):
    __addresses = [fpa.format_with_checksum(__a) for __a in incomplete_addresses]
    assert all([type(__a) == str for __a in __addresses])
    assert all([len(__a) == 42 for __a in __addresses])

def test_address_checksum():
    assert fpa.format_with_checksum('0x00FC00900000002C00BE4EF8F49c000211000c43') != '0x00FC00900000002C00BE4EF8F49c000211000c43'.lower()
    assert fpa.format_with_checksum('0x00FC00900000002C00BE4EF8F49c000211000c43') != '0x00FC00900000002C00BE4EF8F49c000211000c43'.upper()
