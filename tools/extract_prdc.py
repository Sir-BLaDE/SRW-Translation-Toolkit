# -*- coding: utf-8 -*-
"""Extrae valores PRDC de los CPK MtZkn originales."""
import glob
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

for p in sorted(glob.glob(r"C:/Dev/Default Project/srwv/backup/MtZkn_*_original.cpk")):
    cf = load(p)
    vals = set()
    for f in cf.rows:
        d = bytes(b ^ 0x5E for b in cf.plain(f))
        pos = 0
        while True:
            i = d.find(b"PRDC", pos)
            if i < 0:
                break
            q = i + 4
            if q < len(d) and d[q+1:q+4] == b"^^^":
                ln = d[q]
                try:
                    vals.add(d[q+4:q+4+ln].decode("utf-8"))
                except Exception:
                    pass
            pos = q
    print("\n", p, len(vals))
    for v in sorted(vals):
        print(repr(v))
