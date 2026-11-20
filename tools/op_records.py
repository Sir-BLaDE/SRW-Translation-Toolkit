# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK"
cf = load(P)
pt = cf.plain(cf.rows[0])
start = 0x1e0194
for k in range(14):
    rec = pt[start + k * 0x60:start + (k + 1) * 0x60]
    txt = "".join(chr(b) if 32 <= b < 127 else "." for b in rec)
    print("%02d %06x %s" % (k, start + k * 0x60, txt))
    print("   " + " ".join("%02x" % b for b in rec[:48]))
