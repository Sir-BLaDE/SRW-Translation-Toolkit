# -*- coding: utf-8 -*-
"""Diagnostica el crecimiento de la fila 594 de STGEST."""
import io
import json
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"C:/Dev/Default Project/srwv/backup/STGEST_EN_original.cpk"
D = r"C:/Dev/Default Project/srwv/datos"
c = load(P)
f = [r for r in c.rows if r["id"] == 594][0]
pt = c.plain(f).decode("utf-8", "replace")
br = json.load(io.open(D + "/stgest_bracket_es.json", encoding="utf-8"))
items = []
for en, es in br.items():
    old = "[[" + en + "]]"
    if old in pt:
        items.append((pt.count(old), len(en.encode("utf-8")),
                      len(es.encode("utf-8")), en, es))
items.sort(key=lambda x: -(x[2] - x[1]) * x[0])
print("ocurrencias", sum(x[0] for x in items), "delta total",
      sum((x[2] - x[1]) * x[0] for x in items))
for n, le, ls, en, es in items[:15]:
    print("\n--- x%d delta=%d ---" % (n, (ls - le) * n))
    print("EN:", repr(en[:180]))
    print("ES:", repr(es[:220]))
