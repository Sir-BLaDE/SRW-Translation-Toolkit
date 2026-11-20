# -*- coding: utf-8 -*-
"""Busca 'Martian Successor' en todos los CPK instalados (UTF-8 y XOR 0x5E)."""
import glob
import os
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

G = r"D:/Juegos/-SPARROW-/Super Robot Wars V"
patterns = [r"Data/AIDDATA/EN/*.cpk", r"Data/BTLC/EN0/*.CPK",
            r"CommonData/MtData/EN/*.cpk", r"CommonData/ShiroData/LanguageData/EN/*.cpk",
            r"KURODATA/EN/*.CPK", r"STAGE/*.CPK", r"DLCDIRE/EN/*.cpk"]
files = []
for pat in patterns:
    files += glob.glob(os.path.join(G, pat))

for p in files:
    try:
        cf = load(p)
    except Exception:
        continue
    for r in cf.rows:
        pt = cf.plain(r)
        for xor in (0, 0x5E):
            d = pt if xor == 0 else bytes(b ^ xor for b in pt)
            for needle in (b"Martian Successor", b"Martian"):
                start = 0
                while True:
                    i = d.find(needle, start)
                    if i < 0:
                        break
                    print("\n%s | fila %s | xor=%s" % (os.path.basename(p), r["id"], hex(xor)))
                    print(repr(d[max(0, i-160):i+220].decode("utf-8", "replace")))
                    start = i + 1
