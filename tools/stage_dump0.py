"""Vuelca el contenido descifrado del primer bloque de STGEST_EN y mide consumo real."""
import struct

from srwv_cpk import Cpk
from crilayla import ReverseBitReader, _read_match_length, PREFIX_SIZE
from srwv_crypto import decrypt_data


def inflate(payload, prefix, body_size):
    out = bytearray(body_size + PREFIX_SIZE)
    out[:PREFIX_SIZE] = prefix
    reader = ReverseBitReader(payload)
    wi = len(out) - 1

    def put(v):
        nonlocal wi
        out[wi] = v
        wi -= 1
        return wi == PREFIX_SIZE - 1

    while wi >= PREFIX_SIZE:
        if reader.read(1) == 0:
            if put(reader.read(8)):
                break
        else:
            off = reader.read(13)
            length = _read_match_length(reader)
            ri = wi + off + 3
            while length > 0:
                b = out[ri]
                ri -= 1
                length -= 1
                if put(b):
                    break
    return bytes(out), reader.index, reader.bit_count


p = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/STAGE/STGEST_EN.CPK'
c = Cpk(p)
base = 8128
body, comp = struct.unpack_from('<II', c.raw, base + 8)
payload = c.raw[base + 16:base + 16 + comp]
prefix = c.raw[base + 16 + comp:base + 16 + comp + 256]
out, idx, bc = inflate(payload, prefix, body)
print('body', body, 'comp', comp, 'bytes leidos del payload:', comp - idx - 1, 'sobrantes', idx + 1, 'bc', bc)
pt = decrypt_data(out)
print('plain len', len(pt))
# volcar strings
import re
strings = re.findall(rb'[\x20-\x7e]{4,}', pt)
print('n strings', len(strings))
with open('C:/Dev/Default Project/srwv/datos/stgest_block0.txt', 'wb') as f:
    f.write(pt)
for s in strings[:60]:
    print(s[:100])
