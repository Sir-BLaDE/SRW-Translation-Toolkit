# -*- coding: utf-8 -*-
"""Construye KPACK LN traduciendo solo los ids indicados."""
import io
import json
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
import kpack_ln as kln
from srwv_cpkbuild2 import build_ordered

SRC = r"C:/Dev/Default Project/srwv/backup/KPACK_P4_LN_EN_original.cpk"
D = r"C:/Dev/Default Project/srwv/datos"
IDS = set(int(x) for x in (sys.argv[1] if len(sys.argv) > 1 else "0,1,3").split(","))
OUT = sys.argv[2] if len(sys.argv) > 2 else r"C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_id3_compact.cpk"

m0 = json.load(io.open(D + "/ln_id0_es.json", encoding="utf-8"))
m1 = json.load(io.open(D + "/ln_id1_es.json", encoding="utf-8"))
m3 = json.load(io.open(D + "/ln_id3_compact_es.json", encoding="utf-8"))

cf = load(SRC)
new_files = {}

if 0 in IDS:
    f = [x for x in cf.rows if x["id"] == 0][0]
    recs = kln.parse0(cf.plain(f))
    for r in recs:
        s = r["text"].decode("utf-8", "replace")
        if s in m0:
            r["text"] = m0[s].encode("utf-8")
    pt = kln.build0(recs)
    pt += b"\x00" * (len(cf.plain(f)) - len(pt))
    new_files[0] = (cf.cipher(f, pt), len(pt))

if 1 in IDS:
    f = [x for x in cf.rows if x["id"] == 1][0]
    orig = cf.plain(f)
    d = kln.parse1(orig)
    for i, s in enumerate(d["strs"]):
        t = s.decode("utf-8", "replace")
        if t in m1:
            d["strs"][i] = m1[t].encode("utf-8")
    pt = kln.build1(d)
    pt += b"\x00" * (len(orig) - len(pt))
    new_files[1] = (cf.cipher(f, pt), len(pt))

if 3 in IDS:
    f = [x for x in cf.rows if x["id"] == 3][0]
    orig = cf.plain(f)
    strs, _ = kln.parse3(orig)
    new = [m3[s.decode("utf-8", "replace")].encode("utf-8")
           if s.decode("utf-8", "replace") in m3 else s for s in strs]
    pt = kln.build3(new)
    pt += b"\x00" * (len(orig) - len(pt))
    new_files[3] = (cf.cipher(f, pt), len(pt))

# Los ids no seleccionados se copian byte a byte del original.
for f in cf.rows:
    if f["id"] not in new_files:
        new_files[f["id"]] = (cf.raw(f), f["ex"])

blob = build_ordered(SRC, new_files)
open(OUT, "wb").write(blob)
c2 = load(OUT)
for r in c2.rows:
    assert r["ex"] == len(c2.plain(r)), (r["id"], r["ex"], len(c2.plain(r)))
print("escrito", OUT, len(blob), "ids", sorted(IDS), "verificado")

