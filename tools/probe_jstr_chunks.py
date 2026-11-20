# -*- coding: utf-8 -*-\n"""Recorre los chunks de rpw_jstr y describe cada uno."""
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/rpw_jstr.cpk"
c = load(P)
pt = c.plain(c.rows[0])

pos = 0
while True:
    i = pt.find(b"<chunk-head>", pos)
    if i < 0:
        break
    name = pt[i + 16:i + 24]
    nxt, ln = struct.unpack_from("<2I", pt, i + 24)
    print("chunk en", hex(i), "nombre", name, "next", hex(nxt), "len", ln,
          "| data@", hex(i + 32), "hasta", hex(i + 32 + ln))
    pos = i + 32 + ln
print("fin", hex(len(pt)))
