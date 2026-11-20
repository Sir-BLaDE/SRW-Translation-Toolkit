# -*- coding: utf-8 -*-
"""Busca dialogo real (frases con espacios) en un CPK DLC."""
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

G = r"D:/Juegos/-SPARROW-/Super Robot Wars V/"
for name in ("dlc003_en.cpk", "dlc330_en.cpk"):
    c = load(G + "Data/DLCDIRE/EN/" + name)
    print("====", name)
    total = 0
    shown = 0
    for f in c.rows:
        pt = c.plain(f)
        for m in re.finditer(rb'"([^"\\\r\n]{12,})"', pt):
            s = m.group(1)
            try:
                t = s.decode("utf-8")
            except Exception:
                continue
            if re.search(r"[A-Za-z]{3}", t) and (" " in t or "." in t or "!" in t):
                total += 1
                if shown < 15:
                    print("   ", repr(t[:120]))
                    shown += 1
    print("   frases candidatas:", total)
