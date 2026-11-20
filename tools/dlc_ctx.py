# -*- coding: utf-8 -*-
"""Muestra el contexto de una cadena dentro de los DLC."""
import glob
import os
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

needle = sys.argv[1]
files = sorted(glob.glob(r"C:/Dev/Default Project/srwv/backup/dlc_en/dlc*.cpk"))
shown = 0
for p in files:
    c = load(p)
    for r in c.rows:
        try:
            txt = c.plain(r).decode("utf-8")
        except Exception:
            continue
        i = txt.find(needle)
        if i >= 0:
            a = max(0, i - 300)
            print("=== %s row %d" % (os.path.basename(p), r["id"]))
            print(txt[a:i + len(needle) + 300].replace("\r", ""))
            shown += 1
            if shown >= 3:
                sys.exit(0)
print("no encontrado")
