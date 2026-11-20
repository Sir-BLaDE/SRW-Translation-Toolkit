# -*- coding: utf-8 -*-
"""Analiza el pool jstr-zkn de lega_zkn.cpk y sus referencias."""
import re
import struct
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/lega_zkn.cpk"
cf = load(P)
pt = cf.plain(cf.rows[0])
POOL = 0x48
PEND = 0x3F02
strs = []
pos = POOL
while pos < PEND:
    end = pt.find(b"\0", pos)
    if end < 0:
        print("sin NUL en", hex(pos))
        break
    strs.append((pos, pt[pos:end]))
    pos = end + 1
print("cadenas", len(strs), "fin", hex(pos))
starts = {o for o, _ in strs}
# Referencias u32 a offsets del pool desde fuera del propio pool
refs = 0
samples = []
for i in range(0, len(pt) - 3, 4):
    if POOL <= i < PEND:
        continue
    v = struct.unpack_from("<I", pt, i)[0]
    if v in starts:
        refs += 1
        if len(samples) < 20:
            samples.append((hex(i), hex(v), pt[v:v+40].split(b"\0")[0][:40]))
print("refs u32 a inicios de cadena fuera del pool:", refs)
print("muestras", samples[:10])
# cadenas con letras inglesas
print("\n-- cadenas con letras --")
for o, raw in strs:
    if not re.search(rb"[A-Za-z]{3}", raw):
        continue
    s = raw.decode("utf-8", "replace")
    j = o + len(raw)
    while j < PEND and pt[j] == 0:
        j += 1
    print("%06x len=%3d espacio=%3d %r" % (o, len(raw), j - o, s[:100]))
