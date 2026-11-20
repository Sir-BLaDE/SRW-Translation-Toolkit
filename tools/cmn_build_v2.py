# -*- coding: utf-8 -*-
"""Constructor CMN00 correcto (BLTU con cabecera remapeada).

Formato confirmado (CMN00 row 1):
  header: 12 u32 = {6, 0x10, 0x30, 0, 0, 0x20, rel2, rel3, rel4, rel5, total-0x30, 0}
  donde relN = offset_del_chunk_N - 0x30 (chunks 2..5) y los chunks son
  count u32 + count offsets u32 + blob NUL, alineado a 16.

Con traducciones vacias debe reproducir el fichero original byte a byte.
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


def build(orig, trans):
    t = load_bltu(orig)
    header = list(t.header)
    out = bytearray(struct.pack("<12I", *header))
    start = header[2] or 0x30
    while len(out) < start:
        out += b"\0"

    offs_new = []
    for ch in t.chunks:
        offs_new.append(len(out))
        blob = bytearray()
        offs = []
        for s in ch.strings:
            offs.append(len(blob))
            blob += trans.get(s, s).encode("utf-8") + b"\0"
        block = bytearray(struct.pack("<I", len(offs)))
        for o in offs:
            block += struct.pack("<I", o)
        block += blob
        while len(block) % 16:
            block += b"\0"
        out += block

    assert len(t.chunks) == 6, len(t.chunks)
    for i in range(4):
        header[6 + i] = offs_new[2 + i] - start
    header[10] = len(out) - start
    struct.pack_into("<12I", out, 0, *header)
    return bytes(out)


def main():
    identity = len(sys.argv) > 1 and sys.argv[1] == "--identity"
    out_path = None if identity else sys.argv[1]
    trans = {}
    if not identity:
        with io.open(CSV, encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                if row["es"].strip():
                    trans[row["en"]] = row["es"]

    cf = load(ORIG)
    row = cf.rows[1]
    orig = cf.plain(row)
    plain = build(orig, trans)
    print("orig %d nuevo %d identico=%s" % (len(orig), len(plain), orig == plain))
    print("hdr", [hex(x) for x in struct.unpack_from("<12I", plain, 0)])
    if out_path and out_path != "--identity":
        blob = build_ordered(ORIG, {1: (cf.cipher(row, plain), len(plain))})
        open(out_path, "wb").write(blob)
        v = load(out_path)
        print("escrito", out_path, "ex", v.rows[1]["ex"])


if __name__ == "__main__":
    main()
