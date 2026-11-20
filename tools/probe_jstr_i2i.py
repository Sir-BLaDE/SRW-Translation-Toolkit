# -*- coding: utf-8 -*-\n"""Analiza el chunk jstr-i2i de rpw_jstr."""
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/rpw_jstr.cpk"
c = load(P)
pt = c.plain(c.rows[0])
start, end = 0x1ee58, 0x3bce8
d = pt[start:end]
print("i2i len", len(d))
print("hex 0..128")
print(d[:128].hex(" "))
print()
for w in (8, 12, 16, 20, 24):
    print("si entrada=%d -> %d entradas" % (w, len(d) // w))
# interpretar como u32 plano
u = struct.unpack_from("<32I", d, 0)
print("primeros u32:", [hex(x) for x in u])
print()
print("ascii runs:")
import re
for m in re.finditer(rb"[ -~]{4,}", d):
    print("   ", hex(start + m.start()), repr(m.group()[:80]))
    if m.start() > 400:
        break
