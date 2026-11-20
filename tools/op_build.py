# -*- coding: utf-8 -*-
"""Traduce los roles/afiliaciones de OP.CPK sustituyendo las cadenas en el sitio.

Se conserva exactamente la longitud de cada region (cadena + NULs), por lo que
no se desplaza ni un solo byte del resto de la fila.
"""
import os
import shutil
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")

from cpk_util import load
from srwv_cpkbuild2 import build_ordered

G = r"D:/Juegos/-SPARROW-/Super Robot Wars V"
SRC = r"C:/Dev/Default Project/srwv/backup/OP_CK_original.cpk"
BAK = r"C:/Dev/Default Project/srwv/backup/OP_CK_original.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/OP_CK_es.cpk"

# Solo terminos visibles que no son nombres propios. Se priorizan los terms
# ya aprobados en el glosario (Sucesor Marciano, Capitan, ...).
MAP = {
    "Jupiter Empire Soldier": "Soldado de Jupiter",
    "Martian Successor": "Sucesor Marciano",
    "Neo Zeon Soldier": "Soldado de Zeon",
    "Federation Soldier": "Soldado federal",
    "Wolfgang Subordinate": "Subalterno Wolfgang",
    "Gamillas Captain": "Cap. Gamillas",
    "High Spec AI": "IA superior",
    "Analyzer": "Analista",
    "Tenth Angel": "10. Angel",
    "Metal Beast": "Bestia Mec",
    "AI": "IA",
}


def replace_in_place(pt):
    n = 0
    for en, es in MAP.items():
        needle = en.encode("ascii")
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
            while j < len(pt) and pt[j] == 0:
                j += 1
            region = j - i
            if len(new) + 1 > region:
                raise ValueError("no cabe %r -> %r (%d > %d)" % (en, es, len(new) + 1, region))
            pt[i:j] = new + b"\0" * (region - len(new))
            n += 1
            pos = i + len(new)
    return n


if not os.path.exists(BAK):
    shutil.copy2(SRC, BAK)
    print("backup creado", BAK)

cf = load(SRC)
new_files = {}
total = 0
for r in cf.rows:
    pt = bytearray(cf.plain(r))
    before = len(pt)
    n = replace_in_place(pt)
    assert len(pt) == before
    print("fila", r["id"], "sustituciones", n, "longitud", before)
    total += n
    new_files[r["id"]] = (cf.cipher(r, bytes(pt)), before)

out = build_ordered(SRC, new_files)
with open(OUT, "wb") as f:
    f.write(out)
print("escrito", OUT, len(out), "sustituciones totales", total)

chk = load(OUT)
print("diag", chk.cpk.diagnose() or "ok")
for r in chk.rows:
    pt = chk.plain(r)
    print("fila", r["id"], "ex", r["ex"], "len", len(pt), "igual", r["ex"] == len(pt))
    for en in MAP:
        if en.encode() in pt:
            print("  RESTO", en)
