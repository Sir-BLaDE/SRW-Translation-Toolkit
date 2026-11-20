# -*- coding: utf-8 -*-
"""Corrige fragmentos EN partidos por saltos de linea en rpw_jstr_es.json."""
import io
import json
import re

P = r"C:/Dev/Default Project/srwv/datos/rpw_jstr_es.json"
tm = json.load(io.open(P, encoding="utf-8"))
TER = {
    "Air": "Aire",
    "Grd": "Tierra",
    "Wtr": "Agua",
}
pat = re.compile(r"All non-exclusive units(\s+)move as if in (Air|Grd|Wtr)\.")
n = 0
for k, v in list(tm.items()):
    def rep(m):
        return ("Todas las unidades no exclusivas" + m.group(1) +
                "se mueven como si estuvieran en " + TER[m.group(2)] + ".")
    out = pat.sub(rep, v)
    if out != v:
        tm[k] = out
        n += 1
with io.open(P, "w", encoding="utf-8", newline="\n") as f:
    json.dump(tm, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("valores corregidos:", n)
