# -*- coding: utf-8 -*-
"""Mide reutilizacion de traducciones existentes para la lista de rpw_jstr."""
import glob
import io
import json
import os

W = json.load(io.open(r"C:/Dev/Default Project/srwv/datos/rpw_jstr_worklist.json",
                     encoding="utf-8"))
keys = set(W)

maps = {}
for p in sorted(glob.glob(r"C:/Dev/Default Project/srwv/datos/*.json")):
    b = os.path.basename(p)
    if b == "rpw_jstr_worklist.json":
        continue
    try:
        d = json.load(io.open(p, encoding="utf-8"))
    except Exception:
        continue
    if not isinstance(d, dict):
        continue
    good = {k: v for k, v in d.items() if isinstance(k, str) and isinstance(v, str)}
    if good:
        maps[b] = good

union = {}
for b, d in maps.items():
    c = len(keys & set(d))
    if c:
        print("%-45s pares=%-6d cubre=%d" % (b, len(d), c))
        for k in keys & set(d):
            union.setdefault(k, d[k])

print()
print("UNION cubre %d de %d (%.1f%%)" % (len(union), len(keys), 100.0 * len(union) / len(keys)))
long_keys = [k for k in keys if len(k) >= 15]
print("largos(>=15) cubiertos %d de %d" % (sum(1 for k in long_keys if k in union), len(long_keys)))

json.dump(union, io.open(r"C:/Dev/Default Project/srwv/datos/rpw_jstr_reuse.json", "w",
                        encoding="utf-8", newline="\n"),
          ensure_ascii=False, indent=0, sort_keys=True)
print("escrito datos/rpw_jstr_reuse.json")

rest = sorted(keys - set(union), key=lambda s: (-len(s), s))
json.dump(rest, io.open(r"C:/Dev/Default Project/srwv/datos/rpw_jstr_pending.json", "w",
                       encoding="utf-8", newline="\n"),
          ensure_ascii=False, indent=0)
print("pendientes:", len(rest))
