# -*- coding: utf-8 -*-
"""Analiza la estructura de chunks de lega_zkn.cpk."""
import struct
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/lega_zkn.cpk"
cf = load(P)
pt = cf.plain(cf.rows[0])
print("len", len(pt))
for j in range(0, 0x80, 16):
    print("%06x  %-47s  %s" % (j, " ".join("%02x" % b for b in pt[j:j+16]),
          "".join(chr(b) if 32 <= b < 127 else "." for b in pt[j:j+16])))
print("header u32", [hex(struct.unpack_from("<I", pt, i)[0]) for i in (0x20, 0x24)])
for marker in (b"<chunk-head>", b"<chunk-foot>", b"<endofchunk>", b"<file--foot>", b"<end-of-mt>"):
    offs = []
    i = 0
    while True:
        i = pt.find(marker, i)
        if i < 0:
            break
        offs.append(i)
        i += 1
    print(marker.decode(), [hex(x) for x in offs])
for i in [m.start() for m in __import__("re").finditer(b"<chunk-head>", pt)]:
    name = pt[i+16:i+24].rstrip(b"\0")
    a, b = struct.unpack_from("<II", pt, i+24)
    print("chunk", name, "at", hex(i), "next", a, "len", b, "fin", hex(i+32+b))
