#!/usr/bin/env python3
"""CRILAYLA compress - final attempt with bit stream reversal"""

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

def compress(src):
    """Compress using all-literals. Write tokens in forward data order, then reverse bit stream."""
    tokens = []
    for i in range(len(src)):
        tokens.append((0, src[i]))
    
    writer = BitWriter()
    for marker, val in tokens:
        writer.write(0, 1)
        writer.write(val, 8)
    
    # Reverse the bit stream
    bits = writer.bits[:]
    bits = bits[::-1]
    writer.bits = bits
    payload = writer.get_bytes()
    
    body_size = len(src)
    comp_size = len(payload)
    prefix = b'\0' * PREFIX_SIZE
    compressed = MAGIC + struct.pack('<II', body_size, comp_size) + payload + prefix
    return compressed

if __name__ == '__main__':
    from crilayla import maybe_decompress, is_crilayla
    
    tests = [b'Hello World! Test data. ABCDEF.', b'A', b'AB', b'ABC', b'AAAA', b'Hi!']
    for t in tests:
        comp = compress(t)
        try:
            dec = maybe_decompress(comp)
            ok = dec == t
            print(f'{"OK" if ok else "FAIL"}: {t!r}')
            if not ok:
                print(f'   dec={dec}')
        except Exception as e:
            print(f'FAIL: {t!r} - {e}')
