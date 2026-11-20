# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK"
cf = load(P)
for ri, r in enumerate(cf.rows):
    pt = cf.plain(r)
    print("==== FILA", ri, "len", len(pt))
    for needle in (b"Jupiter Empire Soldier", b"Martian Successor", b"Neo Zeon Soldier",
                   b"Gamillas Captain", b"High Spec AI", b"Analyzer", b"Amuro", b"Akito"):
        start = 0
        while True:
            i = pt.find(needle, start)
            if i < 0:
                break
            lo = max(0, i - 48)
            hi = min(len(pt), i + len(needle) + 64)
            print(needle.decode(), "offset", hex(i))
            for j in range(lo, hi, 16):
                chunk = pt[j:j+16]
                print("  %06x  %-47s  %s" % (j, " ".join("%02x" % b for b in chunk),
                      "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)))
            start = i + 1
