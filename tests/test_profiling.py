"""Test the agent on a fork"""

import pstats
import pytest
import web3

import forta_toolkit.profiling as fp
import tests.test_data as td

# FIXTURES ####################################################################

@pytest.fixture
def provider():
    return web3.Web3(web3.HTTPProvider('https://eth.llamarpc.com'))

@pytest.fixture
@fp.profile
def some_process(provider):
    [provider.eth.get_transaction(__t['hash']) for __t in td.ALL_TRANSACTIONS[:16]]

# PROFILING ###################################################################

def test_profile(some_process):
    __p = pstats.Stats('some_process')
    __p.strip_dirs().sort_stats('cumulative')
    assert len(__p.stats.keys()) >= 32

# MAIN ########################################################################

if __name__ == '':
    test_performances()
    display_performances()
