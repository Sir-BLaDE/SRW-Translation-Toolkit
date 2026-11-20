# -*- coding: utf-8 -*-\n"""Actualiza terminos Newtype en LT00 (CSV compartido y CPK intermedio)."""
import csv
import io
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from lt00 import load as load_lt, Lt00
from srwv_cpkbuild2 import build_ordered

CSV = r"C:/Dev/Default Project/srwv/datos/lt00_pendientes.csv"
CPK = r"C:/Dev/Default Project/srwv/outputs/LT00_EN_es.cpk"

REPL = [
    ("Artificial Newtype L", "Nuevo Tipo artificial L"),
    ("Artificial Newtype", "Nuevo Tipo artificial"),
    ("Newtype Artificial L", "Nuevo Tipo artificial L"),
    ("Newtype Artificial", "Nuevo Tipo artificial"),
    ("Newtype L", "Nuevo Tipo L"),
    ("Newtype", "Nuevo Tipo"),
]

def fix(s):
    out = s
    for a, b in REPL:
        out = out.replace(a, b)
    return out

# CSV
rows = list(csv.DictReader(io.open(CSV, encoding="utf-8", newline="")))
n = 0
for r in rows:
    v = fix(r["actual"])
    if v != r["actual"]:
        r["actual"] = v
        n += 1
with io.open(CSV, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["idx", "en", "actual"])
    w.writeheader()
    w.writerows(rows)
print("CSV filas:", n)

# CPK intermedio
cf = load(CPK)
f = cf.rows[0]
t = load_lt(cf.plain(f))
strings = list(t.strings)
m = 0
for i, s in enumerate(strings):
    v = fix(s) if s.startswith("Newtype") or s.startswith("Artificial Newtype") else s
    if v != s:
        strings[i] = v
        m += 1
plain = Lt00(t.raw).build(strings)
blob = cf.cipher(f, plain)
out = build_ordered(CPK, {f["id"]: (blob, len(plain))})
with io.open(CPK, "wb") as fh:
    fh.write(out)
print("CPK cadenas:", m, "ex:", len(plain))
