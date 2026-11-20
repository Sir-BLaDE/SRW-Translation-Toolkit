# -*- coding: utf-8 -*-
"""Inventario de cadenas ASCII en LayoutData.cpk con su espacio NUL disponible."""
import re
import sys
from collections import Counter
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/LayoutData.cpk"
c = load(P)
pt = c.plain(c.rows[0])
seen = {}
for m in re.finditer(rb"[ -~]{3,}\x00", pt):
    s = m.group()[:-1].decode("ascii")
    if not re.search(r"[A-Za-z]{2}", s):
        continue
    i = m.start()
    seen.setdefault(s, []).append(i)

print("cadenas unicas:", len(seen))
for s, offs in sorted(seen.items()):
    # espacio NUL tras la primera aparicion
    i = offs[0]
    j = i + len(s)
    while j < len(pt) and pt[j] == 0:
        j += 1
    pad = j - i - len(s) - 1
    print("%3d pad=%3d %-55r x%d" % (len(s), pad, s[:55], len(offs)))
