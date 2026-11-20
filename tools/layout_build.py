# -*- coding: utf-8 -*-
"""Sustituye cadenas de LayoutData.cpk en el sitio, conservando la longitud
total de cada region (cadena + NULs) para no desplazar la binaria."""
import os
import shutil
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")

from cpk_util import load
from srwv_cpkbuild2 import build_ordered
from layout_map import ES

SRC = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/LayoutData.cpk"
BAK = r"C:/Dev/Default Project/srwv/backup/LayoutData_original.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/LayoutData_es.cpk"

if not os.path.exists(BAK):
    shutil.copy2(SRC, BAK)
    print("backup creado", BAK)

cf = load(SRC)
new_files = {}
total_ok = total_skip = 0
skipped = []
for r in cf.rows:
    pt = bytearray(cf.plain(r))
    before = len(pt)
    for en, es in ES.items():
        needle = en.encode("utf-8")
        new = es.encode("utf-8")
        pos = 0
        while True:
            i = pt.find(needle, pos)
            if i < 0:
                break
            j = i + len(needle)
            if j >= len(pt) or pt[j] != 0:
                pos = i + 1
                continue
            # region = cadena + NULs consecutivos tras ella
            k = j
            while k < len(pt) and pt[k] == 0:
                k += 1
            region = k - i
            if len(new) + 1 > region:
                total_skip += 1
                if len(skipped) < 60:
                    skipped.append((en, len(new) + 1, region))
                pos = i + 1
                continue
            pt[i:k] = new + b"\0" * (region - len(new))
            total_ok += 1
            pos = i + len(new)
    assert len(pt) == before
    new_files[r["id"]] = (cf.cipher(r, bytes(pt)), before)
    print("fila", r["id"], "longitud", before)

blob = build_ordered(SRC, new_files)
with open(OUT, "wb") as f:
    f.write(blob)
print("escrito", OUT, len(blob))
print("sustituciones OK", total_ok, "omitidas (no caben)", total_skip)
for s, need, have in skipped:
    print("  NO CABE %r (%d > %d)" % (s, need, have))

chk = load(OUT)
print("diag", chk.cpk.diagnose() or "ok")
for r in chk.rows:
    pt = chk.plain(r)
    print("fila", r["id"], "ex", r["ex"], "len", len(pt), "igual", r["ex"] == len(pt))
