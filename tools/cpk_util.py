"""cpk_util.py - utilidades de extraccion correctas para los CPK de SRWV.

IMPORTANTE: en los CPK con tablas CpkItocL y CpkItocH el contenido esta
ordenado por ID ascendente mezclando ambas tablas, NO primero L y luego H.
La implementacion anterior (srwv_cpk.file_list) fallaba en CPK grandes.
"""
import struct

from srwv_cpk import Cpk
from crilayla import ReverseBitReader, _read_match_length, PREFIX_SIZE, MAGIC
from srwv_crypto import decrypt_data, encrypt_data
from crilayla_compress_fast import compress


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


class CpkFiles:
    """Vista ordenada por ID con offsets reales."""

    def __init__(self, path):
        self.cpk = Cpk(path)
        info = self.cpk.itoc_info if self.cpk.itoc_offset else {}
        rows = []
        for tn in ('CpkItocL', 'CpkItocH'):
            t = info.get(tn)
            if t is None:
                continue
            for r in range(t.rows_count):
                d = t.row(r)
                rows.append({'id': d['ID'], 'size': d['FileSize'],
                             'ex': d['ExtractSize'], 'table': tn, 'row': r})
        if rows:
            rows.sort(key=lambda x: x['id'])
            off = self.cpk.content_offset
            for f in rows:
                f['offset'] = off
                off += (f['size'] + self.cpk.align - 1) & ~(self.cpk.align - 1)
        else:
            # CPK sin ITOC (p. ej. PrologueImage): la TOC lleva FileOffset
            toc = self.cpk.toc
            if toc is None:
                raise ValueError('el CPK no tiene ITOC ni TOC util')
            for r in range(toc.rows_count):
                d = toc.row(r)
                rows.append({
                    'id': d['ID'], 'size': d['FileSize'], 'ex': d['ExtractSize'],
                    'table': 'CpkToc', 'row': r,
                    'offset': self.cpk.toc_offset + d['FileOffset'],
                })
            rows.sort(key=lambda x: x['id'])
        self.rows = rows

    def raw(self, f):
        return self.cpk.raw[f['offset']:f['offset'] + f['size']]

    def plain(self, f):
        raw = self.raw(f)
        if raw[:8] == MAGIC:
            body, comp = struct.unpack_from('<II', raw, 8)
            data = inflate(raw[16:16 + comp], raw[16 + comp:16 + comp + 256], body)
        else:
            data = raw
        return decrypt_data(data)

    def cipher(self, f, plain):
        """Devuelve el bloque almacenado (CRILAYLA si el original lo estaba)."""
        enc = encrypt_data(plain)
        raw = self.raw(f)
        if raw[:8] == MAGIC:
            return compress(enc)
        return enc


def load(path):
    return CpkFiles(path)
