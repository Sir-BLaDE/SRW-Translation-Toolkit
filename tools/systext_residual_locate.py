# -*- coding: utf-8 -*-
"""Localiza en que fila de SysText estan los residuales EN."""
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/SysText.cpk"
c = load(P)
with open(r"C:/Dev/Default Project/srwv/datos/res_sys_en.txt", encoding="utf-8") as fh:
    targets = set()
    for line in fh:
        if line.startswith("=== "):
            continue
        targets.add(line.rstrip("\n"))

for r in c.rows:
    try:
        pt = c.plain(r)
    except Exception:
        continue
    for part in re.split(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", pt):
        try:
            s = part.decode("utf-8")
        except Exception:
            continue
        if s in targets:
            print("row", r["id"], repr(s))
