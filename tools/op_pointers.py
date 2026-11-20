# -*- coding: utf-8 -*-
"""Busca punteros a las cadenas de OP.CPK dentro de la propia fila."""
import struct
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK"
cf = load(P)
pt = cf.plain(cf.rows[0])
needles = [b"Tobia\x00", b"Jupiter Empire Soldier\x00", b"Akito\x00",
           b"Martian Successor\x00", b"Amuro\x00", b"Neo Zeon Soldier\x00"]
for n in needles:
    off = pt.find(n)
    print(n, hex(off))
    if off < 0:
        continue
    pat = struct.pack("<I", off)
    hits = []
    i = 0
    while True:
        i = pt.find(pat, i)
        if i < 0:
            break
        hits.append(i)
        i += 1
    print("  ptr32_x4 hits", [hex(h) for h in hits[:20]], "total", len(hits))
    # tambien como offset relativo a 0x1e0000 / 0x1e018a
    for base in (0x1e0000, 0x1e018a, 0x1e0194):
        v = off - base
        if v < 0:
            continue
        pat2 = struct.pack("<I", v)
        hits2 = []
        i = 0
        while True:
            i = pt.find(pat2, i)
            if i < 0:
                break
            hits2.append(i)
            i += 1
        if hits2:
            print("  rel base", hex(base), "val", hex(v), "hits", [hex(h) for h in hits2[:10]], "total", len(hits2))
