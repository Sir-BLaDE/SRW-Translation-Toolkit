"""Extrae y vuelca los ficheros internos de STGEST_EN.CPK (Lua bundles)."""
import struct

from srwv_cpk import Cpk
from crilayla import ReverseBitReader, _read_match_length, PREFIX_SIZE
from srwv_crypto import decrypt_data

PATH = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/STAGE/STGEST_EN.CPK'


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
    return bytes(out)


def entries(cpk):
    info = cpk.itoc_info
    rows = []
    for tn in ('CpkItocL', 'CpkItocH'):
        t = info[tn]
        for r in range(t.rows_count):
            d = t.row(r)
            rows.append({'id': d['ID'], 'size': d['FileSize'],
                         'ex': d['ExtractSize'], 'table': tn, 'row': r})
    rows.sort(key=lambda x: x['id'])
    off = cpk.content_offset
    for f in rows:
        f['offset'] = off
        off += (f['size'] + cpk.align - 1) & ~(cpk.align - 1)
    return rows


def extract(cpk, f):
    raw = cpk.raw[f['offset']:f['offset'] + f['size']]
    if raw[:8] == b'CRILAYLA':
        body, comp = struct.unpack_from('<II', raw, 8)
        data = inflate(raw[16:16 + comp], raw[16 + comp:16 + comp + 256], body)
    else:
        data = raw
    return decrypt_data(data)


if __name__ == '__main__':
    cpk = Cpk(PATH)
    rows = entries(cpk)
    print('ficheros', len(rows))
    for f in rows[:4]:
        pt = extract(cpk, f)
        print('=== id', f['id'], 'size', f['size'], 'ex', f['ex'], '-> plain', len(pt))
        print(pt[:160])
        print()
    # volcar los 3 primeros a disco
    for f in rows[:3]:
        open('C:/Dev/Default Project/srwv/outputs/stgest_%d.bin' % f['id'], 'wb').write(extract(cpk, f))
