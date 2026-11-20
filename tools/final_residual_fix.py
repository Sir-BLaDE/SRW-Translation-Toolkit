# -*- coding: utf-8 -*-
"""Corrige los ultimos restos visibles de ingles en LT00 y rpw_jstr."""
import csv
import io
import json
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from lt00 import load as load_lt, Lt00
from srwv_cpkbuild2 import build_ordered

D = r"C:/Dev/Default Project/srwv/datos"

# --- LT00: 6 cadenas visibles con "Newtype" ---
CSV = D + "/lt00_pendientes.csv"
CPK = r"C:/Dev/Default Project/srwv/outputs/LT00_EN_es.cpk"
FIX = {
    "Mejorado por Newtype y sube": "Mejorado por Nuevo Tipo y sube",
    "Las armas Newtype ganan daño igual al nivel de la":
        "Las armas de Nuevo Tipo ganan daño igual al nivel de la",
    "habilidad especial Newtype.": "habilidad especial Nuevo Tipo.",
    "Aumenta en 200 el daño de las armas Newtype y en 10 el CRT.":
        "Aumenta en 200 el daño de las armas de Nuevo Tipo y en 10 el CRT.",
}
rows = list(csv.DictReader(io.open(CSV, encoding="utf-8", newline="")))
n = 0
for r in rows:
    v = FIX.get(r["actual"], r["actual"])
    if v != r["actual"]:
        r["actual"] = v
        n += 1
with io.open(CSV, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["idx", "en", "actual"])
    w.writeheader()
    w.writerows(rows)
print("LT00 CSV filas:", n)

cf = load(CPK)
row = cf.rows[0]
t = load_lt(cf.plain(row))
strings = list(t.strings)
m = 0
for i, s in enumerate(strings):
    v = FIX.get(s, s)
    if v != s:
        strings[i] = v
        m += 1
plain = Lt00(t.raw).build(strings)
out = build_ordered(CPK, {row["id"]: (cf.cipher(row, plain), len(plain))})
with io.open(CPK, "wb") as f:
    f.write(out)
print("LT00 CPK cadenas:", m, "ex:", len(plain))

# --- rpw_jstr: 3 titulos con "Mobile Suit" ---
P = D + "/rpw_jstr_es.json"
tm = json.load(io.open(P, encoding="utf-8"))
NEW = {
    "Mobile Suit Gundam: Char's Counterattack":
        "Traje móvil Gundam: El contraataque de Char",
    "Mobile Suit Gundam: Hathaway's Flash":
        "Traje móvil Gundam: El destello de Hathaway",
    "Mobile Suit Crossbone Gundam: Skull Heart":
        "Traje móvil Crossbone Gundam: Corazón de Calavera",
}
k = 0
for a, b in NEW.items():
    if a in tm and tm[a] != b:
        tm[a] = b
        k += 1
with io.open(P, "w", encoding="utf-8", newline="\n") as f:
    json.dump(tm, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("rpw_jstr titulos:", k)
