"""Format event logs."""

import forta_toolkit._utils
import forta_toolkit.parsing.address

# TRACES ######################################################################

# for __log in logs: __log.topics = tuple(HexBytes(__topic) for __topic in __log.topics)

def parse_log_data(log: dict) -> dict:
    """Flatten and format all the data in an event log."""
    # init
    __data = {
        'block': getattr(log, 'block_number', getattr(log, 'blockNumber', 0)),
        'hash': getattr(log, 'transaction_hash', getattr(log, 'transactionHash', '0x')),
        'index': getattr(log, 'log_index', getattr(log, 'logIndex', 0)),
        'address': forta_toolkit.parsing.address.format_with_checksum(getattr(log, 'address', '')),
        'topics': [forta_toolkit._utils.to_bytes(__t) for __t in getattr(log, 'topics', [])],
        'data': getattr(log, 'data', '0x'),}
    # aliases
    __data['blockHash'] = getattr(log, 'block_hash', getattr(log, 'blockHash', '0x'))
    __data['blockNumber'] = __data['block']
    __data['transactionHash'] = __data['hash']
    __data['transactionIndex'] = getattr(log, 'transaction_index', getattr(log, 'transactionIndex', 0))
    __data['logIndex'] = __data['index']
    # output
    return __data
