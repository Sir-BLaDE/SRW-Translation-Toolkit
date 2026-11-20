#!/usr/bin/env python3
"""Debug CRILAYLA compress/decompress roundtrip"""

from crilayla import decompress, maybe_decompress, is_crilayla, ReverseBitReader, _read_match_length, MAGIC, HEADER_SIZE, PREFIX_SIZE
from crilayla_compress import compress, BitWriter
import struct

def test_compress_decompress(data):
    comp = compress(data)
    dec = maybe_decompress(comp)
    return dec == data, comp, dec

# Test with various data
tests = [
    b'Hello World! Test data. ABCDEF.',
    b'A',
    b'AB',
    b'ABC',
    b'AAAA',
]

for t in tests:
    ok, comp, dec = test_compress_decompress(t)
    print(f'Data: {t!r}')
    print(f'  Compress len: {len(comp)}, Is CRILAYLA: {is_crilayla(comp)}')
    print(f'  BodySize: {struct.unpack_from("<I", comp, 8)[0]}, CompSize: {struct.unpack_from("<I", comp, 12)[0]}')
    print(f'  Decompressed: {dec}')
    print(f'  Match: {dec == t}')
    print()

# Debug the bit reading
data = b'Hello World! Test data. ABCDEF.'
comp = compress(data)
payload = comp[16:16 + struct.unpack_from('<I', comp, 12)[0]]
prefix = comp[16 + struct.unpack_from('<I', comp, 12)[0]:16 + struct.unpack_from('<I', comp, 12)[0] + 256]
body_size = struct.unpack_from('<I', comp, 8)[0]

print('body_size:', body_size, 'len(data):', len(data))
print('comp_size:', struct.unpack_from('<I', comp, 12)[0], 'len(payload):', len(payload))
print('prefix len:', len(prefix))
print('total len:', len(comp))

reader = ReverseBitReader(payload)
marker = reader.read(1)
print('marker:', marker)
literal = reader.read(8)
print('literal:', literal)
