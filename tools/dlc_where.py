# -*- coding: utf-8 -*-
"""Indica en que filas de cada DLC aparece una cadena."""
import glob
import os
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

needle = sys.argv[1]
for p in sorted(glob.glob(r"C:/Dev/Default Project/srwv/backup/dlc_en/dlc*.cpk")):
    c = load(p)
    hits = []
    for r in c.rows:
        try:
            txt = c.plain(r).decode("utf-8")
        except Exception:
            continue
        if needle in txt:
            hits.append((r["id"], txt.count(needle)))
    if hits:
        print("%-16s %s" % (os.path.basename(p), hits))
