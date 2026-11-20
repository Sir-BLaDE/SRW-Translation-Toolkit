# -*- coding: utf-8 -*-
"""Aplica los mapas existentes a B_LT00_EN.cpk y reconstruye el CPK."""
import csv
import glob
import io
import json
import os
import re
import shutil
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load as load_cpk
from lt00 import load as load_lt, Lt00
from srwv_cpkbuild2 import build_ordered

D = r"C:/Dev/Default Project/srwv/datos"
BAK = r"C:/Dev/Default Project/srwv/backup/B_LT00_EN_original.cpk"
GAME = r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/B_LT00_EN_es.cpk"

if not os.path.exists(BAK):
    shutil.copy2(GAME, BAK)
    print("backup creado:", BAK)

cf = load_cpk(BAK)
f = cf.rows[0]
t = load_lt(cf.plain(f))
strings = list(t.strings)
print("B_LT00 original:", len(strings), "cadenas")

# 1) mapa pendientes: alineado por indice (verificado 939/939)
rows = list(csv.DictReader(io.open(D + "/lt00_pendientes.csv", encoding="utf-8", newline="")))
by_idx = {}
for r in rows:
    i = int(r["idx"])
    if strings[i] != r["en"]:
        raise ValueError("desalineacion en indice %d: %r != %r" % (i, strings[i], r["en"]))
    if r["actual"].strip() and r["actual"] != r["en"]:
        by_idx[i] = r["actual"]

# 2) mapa complementario por texto
extra = {}
for name in ("final_lt00_translations_full.txt", "lt00_translations_comprehensive.txt"):
    p = os.path.join(D, name)
    if not os.path.exists(p):
        continue
    with io.open(p, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if "\t" not in line:
                continue
            a, b = line.split("\t", 1)
            if a.strip() and b.strip():
                extra[a.strip()] = b.strip()

# 3) lotes de traduccion nueva (por texto)
new = {}
for p in sorted(glob.glob(os.path.join(D, "b_lt00_rest_es_p*.json"))):
    with io.open(p, encoding="utf-8") as fh:
        new.update(json.load(fh))
print("lotes nuevos:", len(new))

changed_idx = 0
changed_extra = 0
changed_new = 0
for i, s in enumerate(strings):
    if i in by_idx:
        strings[i] = by_idx[i]
        changed_idx += 1
    elif s in new:
        strings[i] = new[s]
        changed_new += 1
    elif s in extra:
        strings[i] = extra[s]
        changed_extra += 1

print("traducidas por indice:", changed_idx, "lotes nuevos:", changed_new,
      "por texto extra:", changed_extra)

plain = Lt00(t.raw).build(strings)
chk = load_lt(plain)
assert chk.strings == strings
assert chk.count == t.count and chk.id_count == t.id_count
print("plain", len(t.raw), "->", len(plain), "cadenas", chk.count, "ids", chk.id_count)

blob = cf.cipher(f, plain)
new_files = {f["id"]: (blob, len(plain))}
out = build_ordered(BAK, new_files)
open(OUT, "wb").write(out)

c2 = load_cpk(OUT)
f2 = c2.rows[0]
pt = c2.plain(f2)
assert pt == plain
assert f2["ex"] == len(pt), (f2["ex"], len(pt))
print("escrito", OUT, len(out), "ex", f2["ex"], "verificado")
