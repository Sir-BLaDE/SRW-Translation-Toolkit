# -*- coding: utf-8 -*-
"""Inventario de texto legible en lega_zkn.cpk (EN)."""
import re
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/lega_zkn.cpk"
cf = load(P)
for r in cf.rows:
    pt = cf.plain(r)
    print("==== FILA", r["id"], "len", len(pt), "ex", r["ex"])
    txt = pt.decode("utf-8", "replace")
    for i, ln in enumerate(txt.split("\n")):
        if re.search(r"[A-Za-z]{3}", ln):
            print("%5d %r" % (i, ln[:160]))
