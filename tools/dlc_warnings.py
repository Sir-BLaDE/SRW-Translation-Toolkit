# -*- coding: utf-8 -*-
"""Recoge avisos de 'posible ingles' en todos los lotes ya traducidos."""
import glob
import io
import json
import os
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from dlc_batch_check import ENG

BATCH = r"C:/Dev/Default Project/srwv/datos/dlc_work/batches"
found = 0
for p in sorted(glob.glob(os.path.join(BATCH, "batch_*.es.json"))):
    src = p.replace(".es.json", ".json")
    try:
        en = json.load(io.open(src, encoding="utf-8"))
        es = json.load(io.open(p, encoding="utf-8"))
    except Exception:
        continue
    for i, (a, b) in enumerate(zip(en, es)):
        if "「" not in a:
            continue
        m = ENG.search(b)
        if m:
            found += 1
            print("%s[%d] %r\n   EN %r\n   ES %r" %
                  (os.path.basename(p), i, m.group(0), a[:110], b[:110]))
print("\navisos de posible ingles:", found)
