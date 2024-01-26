"""Test the agent on a fork"""

import pstats
import pytest
import web3

import toolblocks.parsing.transaction as fpt
import toolblocks.profiling as fp
import tests.test_data as td

# FIXTURES ####################################################################

@pytest.fixture
@fp.profile
def some_process():
    [fpt.parse_transaction_data(__t) for __t in td.ALL_TRANSACTIONS]

# PROFILING ###################################################################

def test_profile(some_process):
    __p = pstats.Stats('some_process')
    __p.strip_dirs().sort_stats('cumulative')
    assert len(__p.stats.keys()) >= 32

# MAIN ########################################################################

if __name__ == '':
    test_performances()
    display_performances()
