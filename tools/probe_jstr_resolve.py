# -*- coding: utf-8 -*-\n"""Resuelve indice -> offset -> cadena en rpw_jstr."""
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/rpw_jstr.cpk"
c = load(P)
pt = c.plain(c.rows[0])
POOL, PEND = 0x48, 0x1ee10
I2I, IEND = 0x1ee58, 0x3bce8


def s_at(off):
    e = pt.find(b"\0", POOL + off)
    return pt[POOL + off:e]


n = (IEND - I2I) // 8
print("entradas", n)
byoff = {}
for i in range(n):
    idx, off = struct.unpack_from("<2I", pt, I2I + i * 8)
    byoff.setdefault(off, []).append(idx)
for i in range(0, 120):
    idx, off = struct.unpack_from("<2I", pt, I2I + i * 8)
    s = s_at(off)
    print("%5d  off=%7d (0x%x)  %r" % (idx, off, off, s[:70]))
