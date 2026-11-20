# -*- coding: utf-8 -*-
"""Compara todos los mapas de traduccion disponibles contra B_LT00."""
import csv
import io
import json
import os
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from lt00 import load as lt

D = r"C:/Dev/Default Project/srwv/datos"
G = r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/"

c = load(G + "B_LT00_EN.cpk")
t = lt(c.plain(c.rows[0]))
strings = t.strings
print("B_LT00 strings:", len(strings))

rows = list(csv.DictReader(io.open(D + "/lt00_pendientes.csv", encoding="utf-8", newline="")))
ok = bad = 0
bad_examples = []
for r in rows:
    i = int(r["idx"])
    if i < len(strings) and strings[i] == r["en"]:
        ok += 1
    else:
        bad += 1
        if len(bad_examples) < 8:
            bad_examples.append((i, r["en"][:50], strings[i][:50] if i < len(strings) else "FUERA"))
print("pendientes idx->en alineados:", ok, "desalineados:", bad)
for x in bad_examples:
    print("   ", x)

# otros mapas: pares en->es
maps = {}
for name in ("final_lt00_translations_full.txt", "final_lt00_translations.txt",
             "lt00_translations_comprehensive.txt", "traducir_lt00.csv"):
    p = os.path.join(D, name)
    if not os.path.exists(p):
        continue
    m = {}
    with io.open(p, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if "\t" in line:
                a, b = line.split("\t", 1)
            elif "=" in line:
                a, b = line.split("=", 1)
            elif "," in line:
                a, b = line.split(",", 1)
            else:
                continue
            if a.strip() and b.strip():
                m[a.strip()] = b.strip()
    maps[name] = m
for name, m in maps.items():
    hits = sum(1 for s in strings if s in m)
    print(name, "pares", len(m), "hits B_LT00", hits)

tm = json.load(io.open(D + "/es_tm.json", encoding="utf-8"))
print("es_tm.json pares", len(tm), "hits", sum(1 for s in strings if s in tm))
with io.open(D + "/lineas_batalla_final_es6.csv", encoding="utf-8", newline="") as fh:
    csvmap = {r["en"]: r["es"] for r in csv.DictReader(fh) if r.get("en") and r.get("es")}
print("lineas_batalla CSV pares", len(csvmap), "hits", sum(1 for s in strings if s in csvmap))
