"""Utility functions for type casting & sanitization."""

# CONVERSIONS #################################################################

def is_raw_hex(data: str) -> bool:
    """Check whether the data is a raw hexadecimal string."""
    try:
        int(data, 16)
        return True
    except Exception:
        return False

def normalize_hexstr(data: str) -> str:
    """Format the hex data in a known and consistent way."""
    return (
        ((len(data) % 2) * '0') # pad so that the length is pair => full bytes
        + data.lower().replace('0x', ''))

def to_hexstr(data: any) -> str:
    """Format any data as a HEX string."""
    __data = ''
    if isinstance(data, str):
        __data = data if is_raw_hex(data=data) else data.encode('utf-8').hex()
    if isinstance(data, bytes):
        __data = data.hex()
    if isinstance(data, int):
        __data = hex(data)
    return normalize_hexstr(__data)

def to_bytes(data: any) -> bytes:
    """Format any data as a bytes array."""
    return bytes.fromhex(to_hexstr(data))