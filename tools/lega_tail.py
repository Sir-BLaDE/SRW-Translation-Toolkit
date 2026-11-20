# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/lega_zkn.cpk"
pt = load(P).plain(load(P).rows[0])
for lo in (0x14420, 0x3ef0):
    hi = min(len(pt), lo + 0xb0)
    print("\n== %06x..%06x ==" % (lo, hi))
    for j in range(lo, hi, 16):
        print("%06x  %-47s  %s" % (j, " ".join("%02x" % b for b in pt[j:j+16]),
              "".join(chr(b) if 32 <= b < 127 else "." for b in pt[j:j+16])))
