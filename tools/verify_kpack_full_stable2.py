# -*- coding: utf-8 -*-
"""Verifica el CPK KPACK LN con los 112 residuales traducidos."""
import hashlib
import io
import json
import os
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
import kpack_ln as k

D = r"C:/Dev/Default Project/srwv/datos"
OUT = r"C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_full_stable2.cpk"
OLD = r"C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_full_stable.cpk"
INST = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK"

en = json.load(io.open(D + "/ln_residual_en.json", encoding="utf-8"))
es = json.load(io.open(D + "/ln_residual_es_list.json", encoding="utf-8"))

c = load(OUT)
bad = []
for f in c.rows:
    p = c.plain(f)
    if len(p) != f["ex"]:
        bad.append((f["id"], len(p), f["ex"]))
print("filas", len(c.rows), "ex_mismatch", len(bad), bad[:5])

rows = {}
for f in c.rows:
    rows[f["id"]] = c.plain(f)

# Estructura preservada
s3, _ = k.parse3(rows[3])
cnt4, recs4 = k.parse4(rows[4])
print("id3 registros", len(s3), "| id4 cabecera", cnt4, "parse4", len(recs4))

# Ningun texto EN residual sobrevive, toda la traduccion ES esta presente
res_en = 0
res_es = 0
for a, b in zip(en, es):
    fid = a["id"]
    if rows[fid].find(a["s"].encode("utf-8")) >= 0:
        res_en += 1
        if res_en <= 5:
            print("  EN sobrevive:", repr(a["s"][:60]))
    if rows[fid].find(b.encode("utf-8")) < 0:
        res_es += 1
        if res_es <= 5:
            print("  ES falta:", repr(b[:60]))
print("EN que sobreviven", res_en, "| ES que faltan", res_es)

# Solo cambiaron las filas esperadas
co = load(OLD)
changed = []
for f in co.rows:
    if c.plain(f) != co.plain(f):
        changed.append(f["id"])
print("filas cambiadas", sorted(changed))


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


print("md5 nuevo    ", md5(OUT))
print("md5 instalado", md5(INST) if os.path.exists(INST) else "NO EXISTE")
