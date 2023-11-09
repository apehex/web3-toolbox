import itertools
import pytest

import forta_toolkit.parsing.logs as fpl
import tests.test_data as td

# FIXTURES ####################################################################

# PARSING #####################################################################

def test_transaction_data_format():
    __data = [fpt.parse_log_data(__l) for __logs in td.ALL_LOGS for __l in __logs]
    assert all([type(__d) == dict for __d in __data])
    assert all([set(__d.keys()) == {'block', 'hash', 'index', 'address', 'topics', 'data'} for __d in __data])
