"""Prueba de extraccion de STGEST_EN: distintas hipotesis de contenedor."""
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
                if ri < PREFIX_SIZE or ri >= len(out):
                    raise ValueError("ref fuera de rango")
                b = out[ri]
                ri -= 1
                length -= 1
                if put(b):
                    break
    return bytes(out)


def score(x):
    if not x:
        return 0
    return sum(1 for t in x if 32 <= t < 127 or t in (9, 10, 13)) / len(x)


def main():
    p = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/STAGE/STGEST_EN.CPK'
    c = Cpk(p)
    fl = c.file_list()
    base = fl[0]['offset']
    body, comp = struct.unpack_from('<II', c.raw, base + 8)
    print('file1 en 0x%X: body=%d comp=%d itoc size=%d extract=%d' % (
        base, body, comp, fl[0]['size'], fl[0]['extract_size']))

    # hipotesis A: leer el payload del CPK completo (desbordando la entrada)
    src = c.raw[base:base + 16 + comp + 256]
    out = inflate(src[16:16 + comp], src[16 + comp:16 + comp + 256], body)
    for name, data in (('plano', out), ('descifrado', decrypt_data(out))):
        print('A', name, 'score', round(score(data), 3), data[:72])


if __name__ == '__main__':
    main()
