# -*- coding: utf-8 -*-
"""OP.CPK valido con acentos en Latin-1 (misma longitud, sin desplazar offsets)."""
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

SRC = r"C:/Dev/Default Project/srwv/backup/OP_CK_original.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/OP_CK_es_acc_latin.cpk"

MAP = {
    "Jupiter Empire Soldier": "Soldado de Júpiter",
    "Martian Successor": "Sucesor Marciano",
    "Neo Zeon Soldier": "Soldado de Zeon",
    "Federation Soldier": "Soldado federal",
    "Wolfgang Subordinate": "Subalterno Wolfgang",
    "Gamillas Captain": "Capitán Gamillas",
    "High Spec AI": "IA superior",
    "Analyzer": "Analista",
    "Tenth Angel": "10.º Ángel",
    "Metal Beast": "Bestia Mec",
    "AI": "IA",
    "Akito": "Akitó",
    "Amuro": "Ámuro",
    "Banjo": "Bánjo",
    "Tobia": "Tobía",
    "Mori": "Morí",
    "Ota": "Otó",
    "Sanada": "Sánada",
}


def replace_in_place(pt):
    n = 0
    for en, es in MAP.items():
        needle = en.encode("ascii")
        new = es.encode("latin-1")
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
open(OUT, "wb").write(out)
print("escrito", OUT, len(out), "sustituciones", total)

chk = load(OUT)
print("diag:", chk.cpk.diagnose() or "ok")
for r in chk.rows:
    p = chk.plain(r)
    print("fila", r["id"], "ex", r["ex"], "len", len(p), "igual", r["ex"] == len(p))
    for name in ("Akitó", "Ámuro", "Bánjo", "Tobía", "Capitán Gamillas"):
        if name.encode("latin-1") in p:
            print("   OK", name)
