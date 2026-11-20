# -*- coding: utf-8 -*-
"""Variante de prueba: traduccion in-situ SOLO con ASCII (sin acentos).

Sirve para aislar si el crash viene de los bytes UTF-8 o del propio texto.
"""
import json
import sys
import unicodedata

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

ORIG = r"C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/Prologue_es_inplace_ascii.cpk"
DATA = r"C:/Dev/Default Project/srwv/datos/prologue_full_v2.json"
TRANS = r"C:/Dev/Default Project/srwv/datos/prologue_trans_v7.json"
META = 22

d = json.load(open(DATA, encoding="utf-8"))
T = json.load(open(TRANS, encoding="utf-8"))


def fold(s):
    s = s.replace("¿", "?").replace("¡", "!")
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if ord(c) < 128 and unicodedata.category(c) != "Mn")


T = {k: fold(v) for k, v in T.items()}


def fit(es, maxbytes):
    b = es.encode("ascii")
    if len(b) <= maxbytes:
        return es, True
    words = es.split()
    while words and len(" ".join(words)) > maxbytes:
        words.pop()
    return " ".join(words), False


def slot_strings(b, meta_start):
    out = []
    i = 0
    while i < meta_start:
        j = b.find(b"\x00", i, meta_start)
        if j < 0:
            break
        if j > i:
            out.append((i, j, b[i:j].decode("utf-8", "ignore")))
        i = j + 1
    return out


c = load(ORIG)
newrows = {}
for r in c.rows:
    pt = bytearray(c.plain(r))
    before = len(pt)
    rid = str(r["id"])
    rd = d.get(rid)
    if not rd:
        newrows[r["id"]] = (c.cipher(r, bytes(pt)), before)
        continue
    cnt, slot = rd["count"], rd["slot"]
    meta = slot - META
    for si in range(cnt):
        base = 24 + si * slot
        b = bytes(pt[base:base + slot])
        spans = slot_strings(b, meta)
        for idx, (a, z, txt) in enumerate(spans):
            key = txt.strip()
            if key not in T or not T[key].strip():
                continue
            nxt = spans[idx + 1][0] if idx + 1 < len(spans) else meta
            maxbytes = nxt - a - 1
            es, _ = fit(T[key].strip(), maxbytes)
            nb = bytearray(maxbytes + 1)
            eb = es.encode("ascii")
            nb[:len(eb)] = eb
            pt[base + a:base + nxt] = nb
    assert len(pt) == before
    newrows[r["id"]] = (c.cipher(r, bytes(pt)), before)

blob = build_ordered(ORIG, newrows)
with open(OUT, "wb") as f:
    f.write(blob)
chk = load(OUT)
assert all(r["ex"] == len(chk.plain(r)) for r in chk.rows)
print("escrito", OUT, len(blob), "ExtractSize OK")
