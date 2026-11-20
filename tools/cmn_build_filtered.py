# -*- coding: utf-8 -*-
"""Constructor CMN00 con filtro de chunks y cabecera corregida.

Uso: python cmn_build_filtered.py <salida.cpk> [--chunks 0,1,2] [--fixhdr] [--hdr10rest]
"""
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
import csv
import io
import struct

from cpk_util import load
from srwv_cpkbuild2 import build_ordered
from srwv_bltu import load as load_bltu

ORIG = r"C:/Dev/Default Project/srwv/backup/CMN00_CPK_original.cpk"
CSV = r"C:/Dev/Default Project/srwv/datos/lineas_batalla_final_es6.csv"


def build(orig, trans, chunks=None):
    t = load_bltu(orig)
    header = t.header
    out = bytearray(struct.pack("<12I", *header))
    start = header[2] or 0x30
    while len(out) < start:
        out += b"\0"

    # posiciones nuevas de cada chunk (para remapear punteros)
    new_off = {}
    for ch in t.chunks:
        new_off[ch.index] = len(out)
        strs = []
        for s in ch.strings:
            if chunks is None or ch.index in chunks:
                strs.append(trans.get(s, s))
            else:
                strs.append(s)
        blob = bytearray()
        offs = []
        for s in strs:
            offs.append(len(blob))
            blob += s.encode("utf-8") + b"\0"
        block = bytearray(struct.pack("<I", len(strs)))
        for o in offs:
            block += struct.pack("<I", o)
        block += blob
        while len(block) % 16:
            block += b"\0"
        out += block

    # mapear offset original -> nuevo offset dentro del fichero
    def remap(old):
        for ch in t.chunks:
            blob_start = ch.offset + 8 + 4 * ch.count
            # longitud real del blob original: hasta el siguiente chunk o fin
            if ch.index + 1 < len(t.chunks):
                blob_end = t.chunks[ch.index + 1].offset
            else:
                blob_end = len(orig)
            if blob_start <= old < blob_end:
                return new_off[ch.index] + 8 + 4 * ch.count + (old - blob_start)
        return old

    # cabecera: punteros 6..9 y tabla en header[5]
    for i in range(6, 10):
        header[i] = remap(header[i])
    tbl = header[5]
    if tbl and tbl + 16 <= len(orig):
        vals = list(struct.unpack_from("<4I", orig, tbl))
        vals = [remap(v) if v else 0 for v in vals]
        struct.pack_into("<4I", out, tbl, *vals)
    header[10] = len(out) - 0x30
    struct.pack_into("<12I", out, 0, *header)
    return bytes(out), t


def main():
    out_path = sys.argv[1]
    chunks = None
    for i, a in enumerate(sys.argv):
        if a == "--chunks":
            chunks = set(int(x) for x in sys.argv[i + 1].split(","))
    trans = {}
    with io.open(CSV, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if row["es"].strip():
                trans[row["en"]] = row["es"]

    cf = load(ORIG)
    row = cf.rows[1]
    orig = cf.plain(row)
    plain, t = build(orig, trans, chunks)
    print("chunks=%s orig=%d nuevo=%d" % (chunks, len(orig), len(plain)))
    blob = build_ordered(ORIG, {1: (cf.cipher(row, plain), len(plain))})
    open(out_path, "wb").write(blob)
    v = load(out_path)
    print("ex", v.rows[1]["ex"], "len", len(plain))
    print("hdr", [hex(x) for x in struct.unpack_from("<12I", plain, 0)])


if __name__ == "__main__":
    main()
