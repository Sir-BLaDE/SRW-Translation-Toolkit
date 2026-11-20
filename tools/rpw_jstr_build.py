# -*- coding: utf-8 -*-
"""Reconstruye rpw_jstr.cpk traduciendo cadenas del pool j-string.

Formato confirmado:
  0x00  <mt> + pad(4)
  0x08  'prod#1' + pad
  0x10  'data#1' + pad
  0x18  '1.00' + pad(4)
  0x20  u32 total-1  -> (len(final)-4)
  0x24  u32 offset del footer final (fin de datos de jstr-i2i)
  0x28  <chunk-head> + pad(4) + 'j-string' + u32 next + u32 len
  0x48  pool de cadenas NUL
  ...   <chunk-foot> (+u64 0x28) + <endofchunk>
        <chunk-head> + pad + 'jstr-i2i' + u32 next + u32 len
        tabla (index,u32 offset) x 14802
        <chunk-foot> (+u64 0x28) + <endofchunk> + <file--foot> (+u64 0x28)
        + '****<end-of-mt>.' + pad(4)

next = len + 72 (72 = 24 chunk-foot + 16 endofchunk + 32 chunk-head).
"""
import io
import json
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

SRC = r"C:/Dev/Default Project/srwv/backup/rpw_jstr_original.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/rpw_jstr_es.cpk"
TM = r"C:/Dev/Default Project/srwv/datos/rpw_jstr_es.json"

POOL = 0x48
PEND = 0x1EE10
I2I = 0x1EE58
IEND = 0x3BCE8

CHUNK_FOOT = b"<chunk-foot>" + b"\0" * 4 + struct.pack("<Q", 0x28)
ENDOFCHUNK = b"<endofchunk>" + b"\0" * 4
FILE_FOOT = b"<file--foot>" + b"\0" * 4 + struct.pack("<Q", 0x28)
END_MT = b"****<end-of-mt>." + b"\0" * 4


def parse_pool(pt):
    out = []
    pos = POOL
    while pos < PEND:
        end = pt.find(b"\0", pos)
        assert end >= 0 and end < PEND + 1, "NUL no encontrado en %d" % pos
        out.append((pos - POOL, pt[pos:end]))
        pos = end + 1
    assert pos == PEND, "pool desalineado: %d" % pos
    return out


def build(pt, trans):
    strs = parse_pool(pt)
    starts = set(off for off, _ in strs)

    # nuevo pool + mapa viejo->nuevo
    pool = bytearray()
    remap = {}
    replaced = 0
    for off, raw in strs:
        try:
            s = raw.decode("utf-8")
        except Exception:
            s = None
        if s is not None and s in trans:
            new = trans[s].encode("utf-8")
            replaced += 1
        else:
            new = raw
        remap[off] = len(pool)
        pool += new + b"\0"

    # i2i
    n = (IEND - I2I) // 8
    i2i = bytearray()
    for i in range(n):
        idx, off = struct.unpack_from("<2I", pt, I2I + i * 8)
        if off not in starts:
            raise SystemExit("i2i offset invalido %d (idx %d)" % (off, idx))
        i2i += struct.pack("<2I", idx, remap[off])

    len1 = len(pool)
    len2 = len(i2i)

    out = bytearray()
    out += pt[:0x20]
    out += struct.pack("<2I", 0, 0)  # placeholder
    out += b"<chunk-head>" + b"\0" * 4 + b"j-string"
    out += struct.pack("<2I", len1 + 72, len1)
    out += pool
    out += CHUNK_FOOT + ENDOFCHUNK
    out += b"<chunk-head>" + b"\0" * 4 + b"jstr-i2i"
    out += struct.pack("<2I", len2 + 72, len2)
    out += i2i
    foot_off = len(out)
    out += CHUNK_FOOT + ENDOFCHUNK + FILE_FOOT + END_MT

    struct.pack_into("<II", out, 0x20, len(out) - 4, foot_off)
    return bytes(out), len1, len2, replaced


def main():
    c = load(SRC)
    pt = c.plain(c.rows[0])
    trans = {}
    try:
        trans = json.load(io.open(TM, encoding="utf-8"))
    except Exception:
        print("sin mapa de traduccion:", TM)
    plain, len1, len2, rep = build(pt, trans)
    print("pool %d -> %d | i2i %d | reemplazos %d | total %d"
          % (len(pt), len(plain), len2, rep, len(plain)))

    row = c.rows[0]
    blob = c.cipher(row, plain)
    out = build_ordered(SRC, {row["id"]: (blob, len(plain))})
    with io.open(OUT, "wb") as f:
        f.write(out)
    print("escrito", OUT)

    # verificacion
    v = load(OUT)
    vp = v.plain(v.rows[0])
    assert vp == plain, "round-trip CPK distinto"
    assert v.rows[0]["ex"] == len(plain), "ExtractSize incorrecto"
    print("verificado: ExtractSize=%d len(plain)=%d" % (v.rows[0]["ex"], len(plain)))


if __name__ == "__main__":
    main()
