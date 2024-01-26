import pytest

from toolblocks.logging import setup_log_format, setup_logger

# FORMAT ######################################################################

def test_setup_format_always_returns_a_string():
    __patterns = (
        setup_log_format(),
        setup_log_format(version='1.2'),
        setup_log_format(pattern='test'),
        setup_log_format(pattern='{version}'),
        setup_log_format(pattern='test', version='0.1'))
    assert all(type(__p) == str for __p in __patterns)

def test_setup_format_includes_dash_only_when_necessary():
    assert '-' not in setup_log_format(version='')
    assert '-' in setup_log_format(version='0.6.1')

# LOGGING #####################################################################

def test_setup_logger_works_without_bot_metadata():
    assert setup_logger() is None # no error
