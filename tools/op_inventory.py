# -*- coding: utf-8 -*-
"""Inventario de cadenas ASCII terminadas en NUL en todos los registros de OP.CPK."""
import re
import sys
from collections import Counter
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK"
cf = load(P)
allc = Counter()
for r in cf.rows:
    pt = cf.plain(r)
    print("==== FILA", r["id"])
    seen = {}
    for m in re.finditer(rb"[ -~]{2,}\x00", pt):
        s = m.group()[:-1].decode("ascii")
        if not re.search(r"[A-Za-z]", s):
            continue
        key = s
        seen.setdefault(key, []).append(m.start())
        allc[key] += 1
    for s, offs in sorted(seen.items()):
        print("  %-32r %4d %s" % (s, len(s.encode()), [hex(x) for x in offs[:6]]))
print("\n==== TOTAL UNICOS", len(allc))
