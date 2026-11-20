#!/usr/bin/env python3
"""CRILAYLA compress - definitive implementation with bit ordering fix"""

from crilayla import ReverseBitReader, MAGIC, HEADER_SIZE, PREFIX_SIZE
import struct

class BitWriter:
    def __init__(self):
        self.bits = []
    def write(self, value, count):
        for i in range(count):
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

def compress(src, token_order='reverse', reverse_bytes=False):
    """Compress using all-literals LZ77.
    
    token_order: 'forward' = data[0],data[1],... ; 'reverse' = data[N-1],...,data[0]
    reverse_bytes: if True, reverse the packed byte array before padding.
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
    if reverse_bytes:
        bits_bytes = bytes(reversed(bits_bytes))
    
    body_size = len(src)
    comp_size = len(bits_bytes)
    prefix = b'\0' * PREFIX_SIZE
    compressed = MAGIC + struct.pack('<II', body_size, comp_size) + bits_bytes + prefix
    return compressed

if __name__ == '__main__':
    from crilayla import maybe_decompress, is_crilayla
    
    tests = [b'Hello World! Test data. ABCDEF.', b'A', b'AB', b'ABC', b'AAAA', b'Hi!']
    for t in tests:
        found = False
        for token_order in ['forward', 'reverse']:
            for reverse_bytes in [False, True]:
                comp = compress(t, token_order, reverse_bytes)
                try:
                    dec = maybe_decompress(comp)
                    if dec == t:
                        print(f'OK: {t!r} token_order={token_order}, reverse_bytes={reverse_bytes}')
                        found = True
                        break
                except Exception as e:
                    pass
        if not found:
            print(f'FAIL: {t!r}')
