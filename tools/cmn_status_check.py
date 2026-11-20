# -*- coding: utf-8 -*-
"""Comprueba el estado de traduccion de los nombres de estado en CMN00."""
import csv
import io
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from srwv_bltu import load as load_bltu

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/CMN00.CPK"
CSV = r"C:/Dev/Default Project/srwv/datos/lineas_batalla_final_es6.csv"

c = load(P)
f1 = c.plain(c.rows[1])
t = load_bltu(f1)
alls = t.all_strings()
print("CMN00 f1 chunks", len(t.chunks), "strings", len(alls))

with io.open(CSV, encoding="utf-8", newline="") as fh:
    m = {}
    for r in csv.DictReader(fh):
        if r.get("en") and r.get("es"):
            m[r["en"]] = r["es"]
print("CSV con traduccion:", len(m))

# primeras 60 cadenas (donde estan los estados)
for idx, chunk, off, s in alls[:60]:
    es = m.get(s, "")
    mark = "OK" if es else "FALTA"
    print("%4d %-6s %-28r => %r" % (idx, mark, s[:28], es[:40]))
