# -*- coding: utf-8 -*-
"""Genera un systext_trans con traducciones solo en el rango de indices dado."""
import json
import sys
from pathlib import Path

D = Path(r"C:/Dev/Default Project/srwv/datos")
lo = int(sys.argv[1])
hi = int(sys.argv[2])
out = Path(sys.argv[3]) if len(sys.argv) > 3 else D / "systext_trans_subset.json"

items = json.loads((D / "systext_row2.json").read_text(encoding="utf-8"))
full = json.loads((D / "systext_trans.json").read_text(encoding="utf-8"))
sub = {}
for x in items:
    if lo <= x["i"] <= hi and x["s"] in full:
        sub[x["s"]] = full[x["s"]]
out.write_text(json.dumps(sub, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("escrito", out, "claves", len(sub), "rango", lo, hi)
