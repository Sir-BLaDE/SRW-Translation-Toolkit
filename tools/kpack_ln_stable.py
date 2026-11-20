# -*- coding: utf-8 -*-
"""KPACK LN con id0/id1/id3 traducidos e id4 intacto (longitud original)."""
import io
import json
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
import kpack_ln as kln
from srwv_cpkbuild2 import build_ordered

SRC = r"C:/Dev/Default Project/srwv/backup/KPACK_P4_LN_EN_original.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_es_stable.cpk"
D = r"C:/Dev/Default Project/srwv/datos"

m0 = json.load(io.open(D + "/ln_id0_es.json", encoding="utf-8"))
m1 = json.load(io.open(D + "/ln_id1_es.json", encoding="utf-8"))
m3 = json.load(io.open(D + "/ln_id3_descs_es.json", encoding="utf-8"))

cf = load(SRC)
new_files = {}

f0 = [f for f in cf.rows if f["id"] == 0][0]
pt0 = cf.plain(f0)
recs0 = kln.parse0(pt0)
for r in recs0:
    s = r["text"].decode("utf-8", "replace")
    if s in m0:
        r["text"] = m0[s].encode("utf-8")
plain0 = kln.build0(recs0)
plain0 += b"\x00" * (len(pt0) - len(plain0))
assert len(kln.parse0(plain0)) == len(recs0)
new_files[0] = (cf.cipher(f0, plain0), len(plain0))

f1 = [f for f in cf.rows if f["id"] == 1][0]
pt1 = cf.plain(f1)
d1 = kln.parse1(pt1)
for i, s in enumerate(d1["strs"]):
    t = s.decode("utf-8", "replace")
    if t in m1:
        d1["strs"][i] = m1[t].encode("utf-8")
plain1 = kln.build1(d1)
plain1 += b"\x00" * (len(pt1) - len(plain1))
new_files[1] = (cf.cipher(f1, plain1), len(plain1))

f3 = [f for f in cf.rows if f["id"] == 3][0]
pt3 = cf.plain(f3)
strs3, _ = kln.parse3(pt3)
new3 = []
for s in strs3:
    t = s.decode("utf-8", "replace")
    new3.append(m3[t].encode("utf-8") if t in m3 else s)
plain3 = kln.build3(new3)
plain3 += b"\x00" * (len(pt3) - len(plain3))
assert len(kln.parse3(plain3)[0]) == len(strs3)
new_files[3] = (cf.cipher(f3, plain3), len(plain3))

blob = build_ordered(SRC, new_files)
open(OUT, "wb").write(blob)
cf2 = load(OUT)
for r in cf2.rows:
    assert r["ex"] == len(cf2.plain(r)), (r["id"], r["ex"], len(cf2.plain(r)))
print("escrito", OUT, len(blob), "verificado")
