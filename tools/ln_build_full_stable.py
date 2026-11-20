# -*- coding: utf-8 -*-
"""KPACK LN: id0/id1/id2/id3 compacto/id4 parcial, todo estable."""
import io
import json
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
import kpack_ln as kln
from srwv_cpkbuild2 import build_ordered

SRC = r"C:/Dev/Default Project/srwv/backup/KPACK_P4_LN_EN_original.cpk"
ID4SRC = r"C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_id4partial3.cpk"
D = r"C:/Dev/Default Project/srwv/datos"
OUT = sys.argv[1] if len(sys.argv) > 1 else r"C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_full_stable.cpk"

ID4 = not (len(sys.argv) > 2 and sys.argv[2] == "noid4")

m0 = json.load(io.open(D + "/ln_id0_es.json", encoding="utf-8"))
m1 = json.load(io.open(D + "/ln_id1_es.json", encoding="utf-8"))
m3 = json.load(io.open(D + "/ln_id3_compact_es.json", encoding="utf-8"))

cf = load(SRC)
c4 = load(ID4SRC)
new_files = {}

def put(fid, pt):
    f = [x for x in cf.rows if x["id"] == fid][0]
    new_files[fid] = (cf.cipher(f, pt), len(pt))

# id0 (el formato permite crecer; las pruebas individuales dieron 8/8)
f0 = [x for x in cf.rows if x["id"] == 0][0]
orig0 = cf.plain(f0)
recs = kln.parse0(orig0)
for r in recs:
    s = r["text"].decode("utf-8", "replace")
    if s in m0:
        r["text"] = m0[s].encode("utf-8")
pt = kln.build0(recs)
assert len(kln.parse0(pt)) == len(recs)
put(0, pt)

# id1 (tabla de offsets: tambien puede crecer)
f1 = [x for x in cf.rows if x["id"] == 1][0]
orig1 = cf.plain(f1)
d = kln.parse1(orig1)
for i, s in enumerate(d["strs"]):
    t = s.decode("utf-8", "replace")
    if t in m1:
        d["strs"][i] = m1[t].encode("utf-8")
pt = kln.build1(d)
assert len(kln.parse1(pt)["strs"]) == len(d["strs"])
put(1, pt)

# id2: descripcion de escenario visible (mismo tamano)
f2 = [x for x in cf.rows if x["id"] == 2][0]
pt2 = c4.plain([x for x in c4.rows if x["id"] == 2][0])
assert len(pt2) == len(cf.plain(f2))
put(2, pt2)

# id3 compacto: se rellena hasta el tamano original para no alterar los callbacks
f3 = [x for x in cf.rows if x["id"] == 3][0]
orig3 = cf.plain(f3)
strs3, _ = kln.parse3(orig3)
new3 = []
for s in strs3:
    t = s.decode("utf-8", "replace")
    new3.append(m3[t].encode("utf-8") if t in m3 else s)
pt = kln.build3(new3)
assert len(pt) <= len(orig3), (3, len(pt), len(orig3))
assert len(kln.parse3(pt)[0]) == len(strs3)
put(3, pt + b"\x00" * (len(orig3) - len(pt)))

# id4 parcial (mismo tamano)
if ID4:
    f4 = [x for x in cf.rows if x["id"] == 4][0]
    pt4 = c4.plain([x for x in c4.rows if x["id"] == 4][0])
    assert len(pt4) == len(cf.plain(f4))
    put(4, pt4)

blob = build_ordered(SRC, new_files)
open(OUT, "wb").write(blob)
c2 = load(OUT)
for r in c2.rows:
    assert r["ex"] == len(c2.plain(r)), (r["id"], r["ex"], len(c2.plain(r)))
print("escrito", OUT, len(blob), "id4", bool(ID4), "verificado")
