import itertools
import pytest

import forta_toolkit.parsing.traces as fpt
import tests.test_data as td

# FIXTURES ####################################################################

# PARSING #####################################################################

def test_transaction_data_format():
    __data = [fpt.parse_trace_data(__t) for __traces in td.ALL_TRACES for __t in __traces]
    assert all([type(__d) == dict for __d in __data])
    assert all([type(__v) == str or type(__v) == int for __d in __data for __v in __d.values()])
    assert all([set(__d.keys()) == {'block', 'hash', 'type', 'value', 'gas', 'from', 'to', 'input', 'output'} for __d in __data])
    assert all([__d.get('type', '') in ('call', 'create', 'suicide', 'delegatecall', 'callcode', 'staticcall') for __d in __data])
