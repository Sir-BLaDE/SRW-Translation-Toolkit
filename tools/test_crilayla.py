#!/usr/bin/env python3
"""Test CRILAYLA compress/decompress roundtrip"""

from crilayla import decompress, maybe_decompress, is_crilayla, ReverseBitReader, _read_match_length
from crilayla_compress import compress_simple, BitWriter
import struct

test_data = b'Hello World! Test data. ABCDEF.'
comp = compress_simple(test_data)
print('Compressed len:', len(comp))
print('Is CRILAYLA:', is_crilayla(comp))
dec = maybe_decompress(comp)
print('Decompressed len:', len(dec))
print('Decompressed data:', dec)
print('Match:', dec == test_data)
