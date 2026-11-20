# -*- coding: utf-8 -*-
"""Corrige 'move as if on Grd.' en rpw_jstr_es.json."""
import io
import json
import re

P = r"C:/Dev/Default Project/srwv/datos/rpw_jstr_es.json"
tm = json.load(io.open(P, encoding="utf-8"))
pat = re.compile(r"All non-exclusive units(\s+)move as if on Grd\.")
n = 0
for k, v in list(tm.items()):
    out = pat.sub(lambda m: "Todas las unidades no exclusivas" + m.group(1) +
                  "se mueven como si estuvieran en Tierra.", v)
    if out != v:
        tm[k] = out
        n += 1
with io.open(P, "w", encoding="utf-8", newline="\n") as f:
    json.dump(tm, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("valores corregidos:", n)
