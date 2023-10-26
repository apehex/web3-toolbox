"""Format transaction traces."""

import hexbytes

import forta_toolkit.parsing.address

# TRACES ######################################################################

def parse_trace_data(trace: dict, get_code: callable) -> dict:
    """Flatten and format all the data in a transaction trace."""
    # common
    __block = getattr(trace, 'block_number', getattr(trace, 'blockNumber', -1))
    __hash = getattr(trace, 'transaction_hash', getattr(trace, 'transactionHash', hexbytes.HexBytes('0x'))).hex()
    __type = getattr(trace, 'type', '')
    __action = getattr(trace, 'action', {})
    __result = getattr(trace, 'result', {})
    __value = getattr(__action, 'value', 0)
    __gas = getattr(__result, 'gas_used', getattr(__result, 'gasUsed', 0))
    # output
    __data = {
        'block': __block,
        'hash': __hash,
        'type': __type,
        'value': __value,
        'gas': __gas,
        'from': '',
        'to': '',
        'input': '',
        'output': ''}
    # call
    if __type == 'call':
        __data['type'] = getattr(__action, 'call_type', getattr(__action, 'callType', 'call')) # actually get the exact variant of the call
        __data['from'] = forta_toolkit.parsing.address.format_with_checksum(getattr(__action, 'from_', getattr(__action, 'from', '')))
        __data['to'] = forta_toolkit.parsing.address.format_with_checksum(getattr(__action, 'to', ''))
        __data['input'] = getattr(__action, 'input', hexbytes.HexBytes('0x')).hex()
        __data['output'] = getattr(__result, 'output', hexbytes.HexBytes('0x')).hex()
    # create
    if __type == 'create':
        __data['from'] = forta_toolkit.parsing.address.format_with_checksum(getattr(__action, 'from_', getattr(__action, 'from', '')))
        __data['to'] = forta_toolkit.parsing.address.format_with_checksum(getattr(__result, 'address', ''))
        __data['input'] = getattr(__action, 'init', hexbytes.HexBytes('0x')).hex()
        __data['output'] = getattr(__result, 'code', hexbytes.HexBytes('0x')).hex()
    # suicide
    if __type == 'suicide':
        __data['from'] = forta_toolkit.parsing.address.format_with_checksum(getattr(__action, 'address', ''))
        __data['to'] = forta_toolkit.parsing.address.format_with_checksum(getattr(__action, 'refund_address', getattr(__action, 'refundAddress', '')))
        __data['input'] = getattr(__action, 'balance', hexbytes.HexBytes('0x')).hex()
        __data['output'] = '0x'
    return __data
