"""Format addresses."""

import eth_utils.address

# ADDRESS #####################################################################

def format_with_checksum(address: str) -> str:
    """Format an address as a HEX string of length 40 with the "0x" prefix and a checksum."""
    return (
        eth_utils.address.to_checksum_address('0x{0:0>40x}'.format(int(address, 16))) if address
        else '')
