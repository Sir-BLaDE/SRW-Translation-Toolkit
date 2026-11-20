#!/usr/bin/env python3
"""Debug CRILAYLA compress - try different bit orderings"""

from crilayla import decompress, maybe_decompress, is_crilayla, ReverseBitReader, MAGIC, HEADER_SIZE, PREFIX_SIZE, _read_match_length
from crilayla_compress import BitWriter
import struct

def make_compressed(src, token_order='reverse', bit_reverse=False):
    """token_order: 'forward' or 'reverse' - order of tokens
       bit_reverse: if True, reverse the bit stream before packing
    """
    tokens = []
    if token_order == 'forward':
        for i in range(len(src)):
            tokens.append((0, src[i]))
    else:
        for i in range(len(src) - 1, -1, -1):
            tokens.append((0, src[i]))
    
    writer = BitWriter()
    for marker, val in tokens:
        writer.write(0, 1)
        writer.write(val, 8)
    
    bits_bytes = writer.get_bytes()
    
    if bit_reverse:
        # Reverse the bits within each byte? Or reverse bytes?
        # Let's reverse the bytes (LSB-first packing means reversing bytes changes order)
        rev_bytes = bytes(reversed(bits_bytes))
        payload = rev_bytes
    else:
        payload = bits_bytes
    
    body_size = len(src)
    prefix = b'\0' * PREFIX_SIZE
    compressed = MAGIC + struct.pack('<II', body_size, len(payload)) + payload + prefix
    return compressed

data = b'Hello World! Test data. ABCDEF.'
for token_order in ['forward', 'reverse']:
    for bit_reverse in [False, True]:
        comp = make_compressed(data, token_order, bit_reverse)
        try:
            dec = maybe_decompress(comp)
            ok = dec == data
            print(f'token_order={token_order}, bit_reverse={bit_reverse}: OK={ok}')
            if ok:
                break
        except Exception as e:
            print(f'token_order={token_order}, bit_reverse={bit_reverse}: FAIL - {e}')

# Let me also try: write bits MSB-first
class BitWriter2(BitWriter):
    def write(self, value, count):
        for i in range(count - 1, -1, -1):
            bit = (value >> i) & 1
            self.bits.append(bit)
    def get_bytes(self):
        while len(self.bits) % 8 != 0:
            self.bits.append(0)
        out = bytearray()
        for i in range(0, len(self.bits), 8):
            byte = 0
            for j in range(8):
                byte |= (self.bits[i + j] << j)
            out.append(byte)
        return bytes(out)

for token_order in ['forward', 'reverse']:
    writer = BitWriter2()
    tokens = []
    if token_order == 'forward':
        for i in range(len(data)):
            tokens.append((0, data[i]))
    else:
        for i in range(len(data) - 1, -1, -1):
            tokens.append((0, data[i]))
    for marker, val in tokens:
        writer.write(0, 1)
        writer.write(val, 8)
    bits_bytes = writer.get_bytes()
    comp = MAGIC + struct.pack('<II', len(data), len(bits_bytes)) + bits_bytes + b'\0' * PREFIX_SIZE
    try:
        dec = maybe_decompress(comp)
        ok = dec == data
        print(f'MSB-first, token_order={token_order}: OK={ok}')
        if ok:
            break
    except Exception as e:
        print(f'MSB-first, token_order={token_order}: FAIL - {e}')
