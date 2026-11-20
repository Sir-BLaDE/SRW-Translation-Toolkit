# -*- coding: utf-8 -*-
"""Genera un mapa id3 con solo las traducciones que caben en su slot original."""
import json
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from kpack_ln import parse3

D = r"C:/Dev/Default Project/srwv/datos"
SRC = r"C:/Dev/Default Project/srwv/backup/KPACK_P4_LN_EN_original.cpk"
OUT = D + "/ln_id3_fit.json"

cf = load(SRC)
pt = cf.plain([x for x in cf.rows if x["id"] == 3][0])
strs, _ = parse3(pt)
sizes = []
p = 0
for s in strs:
    total = struct.unpack_from("<I", pt, p)[0]
    sizes.append(total)
    p += total

T = json.load(open(D + "/ln_id3_descs_es.json", encoding="utf-8"))
out = {}
for s, sz in zip(strs, sizes):
    en = s.decode("utf-8", "replace")
    es = T.get(en)
    if not es:
        continue
    b = es.encode("utf-8")
    need = 4 + ((len(b) + 1 + 3) & ~3)
    if need <= sz:
        out[en] = es
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("escrito", OUT, "traducciones que caben", len(out), "de", len(T))
