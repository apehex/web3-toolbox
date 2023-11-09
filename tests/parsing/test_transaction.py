import itertools
import pytest

import forta_toolkit.parsing.transaction as fpt
import tests.test_data as td

# FIXTURES ####################################################################

# PARSING #####################################################################

def test_transaction_data_format():
    __data = [fpt.parse_transaction_data(__t) for __t in td.ALL_TRANSACTIONS]
    assert all([type(__d) == dict for __d in __data])
    assert all([type(__v) == str for __d in __data for __v in __d.values()])
    assert all([set(__d.keys()) == {'hash', 'from', 'to', 'data', 'value'} for __d in __data])
