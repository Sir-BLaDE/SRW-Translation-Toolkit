# -*- coding: utf-8 -*-
"""KPACK LN: como full_stable + los 112 residuales traducidos.

- fila 0/1/3: se reconstruyen desde el original con sus mapas (id1/id3 ampliados).
- fila 2/4: se toman de id4partial3 y se parchean los residuales en su hueco,
  manteniendo longitud y cabeceras exactamente iguales.
"""
import io
import json
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
import kpack_ln as kln
from srwv_cpkbuild2 import build_ordered

SRC = r"C:/Dev/Default Project/srwv/backup/KPACK_P4_LN_EN_original.cpk"
ID4SRC = r"C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_id4partial3.cpk"
D = r"C:/Dev/Default Project/srwv/datos"
OUT = (sys.argv[1] if len(sys.argv) > 1 else
       r"C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_full_stable2.cpk")

m0 = json.load(io.open(D + "/ln_id0_es.json", encoding="utf-8"))
m1 = json.load(io.open(D + "/ln_id1_es.json", encoding="utf-8"))
m3 = json.load(io.open(D + "/ln_id3_compact_es.json", encoding="utf-8"))
res_en = json.load(io.open(D + "/ln_residual_en.json", encoding="utf-8"))
res_es = json.load(io.open(D + "/ln_residual_es_list.json", encoding="utf-8"))
assert len(res_en) == len(res_es)

# Ampliar los mapas de las filas 1 y 3 con sus residuales
for a, b in zip(res_en, res_es):
    if a["id"] == 1:
        assert a["s"] not in m1 or m1[a["s"]] == b, a["s"]
        m1[a["s"]] = b
    elif a["id"] == 3:
        assert a["s"] not in m3 or m3[a["s"]] == b, a["s"]
        m3[a["s"]] = b

cf = load(SRC)
c4 = load(ID4SRC)
new_files = {}


def put(fid, pt):
    f = [x for x in cf.rows if x["id"] == fid][0]
    new_files[fid] = (cf.cipher(f, pt), len(pt))


def align(v, a):
    return (v + a - 1) & ~(a - 1)


# ---- id0 ----
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

# ---- id1 ----
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

# ---- id2: parchear descripciones en su hueco alineado a 4 ----
f2 = [x for x in cf.rows if x["id"] == 2][0]
orig2 = cf.plain(f2)
pt2 = bytearray(c4.plain([x for x in c4.rows if x["id"] == 2][0]))
assert len(pt2) == len(orig2)
n2 = 0
for a, b in zip(res_en, res_es):
    if a["id"] != 2:
        continue
    old = a["s"].encode("utf-8")
    new = b.encode("utf-8") + b"\0"
    pos = pt2.find(old)
    assert pos >= 0, ("id2 no encontrado", a["s"][:60])
    slot = align(len(old) + 1, 4)
    assert len(new) <= slot, ("id2 no cabe", a["s"][:60])
    # Solo relleno entre el texto original y el final del hueco
    assert all(v == 0 for v in pt2[pos + len(old):pos + slot]), a["s"][:60]
    pt2[pos:pos + slot] = new + b"\0" * (slot - len(new))
    n2 += 1
assert bytes(pt2) != orig2
put(2, bytes(pt2))

# ---- id3 compacto: se rellena hasta el tamano original ----
f3 = [x for x in cf.rows if x["id"] == 3][0]
orig3 = cf.plain(f3)
strs3, _ = kln.parse3(orig3)
new3 = []
for s in strs3:
    t = s.decode("utf-8", "replace")
    new3.append(m3[t].encode("utf-8") if t in m3 else s)
pt = kln.build3(new3)
assert len(pt) <= len(orig3), (3, len(pt), len(orig3))
assert len(kln.parse3(pt)[0]) == len(strs3) == 145
put(3, pt + b"\0" * (len(orig3) - len(pt)))

# ---- id4: prefijo u32 en pos-4, parche en el hueco declarado ----
f4 = [x for x in cf.rows if x["id"] == 4][0]
orig4 = cf.plain(f4)
pt4 = bytearray(c4.plain([x for x in c4.rows if x["id"] == 4][0]))
assert len(pt4) == len(orig4)
n4 = 0
for a, b in zip(res_en, res_es):
    if a["id"] != 4:
        continue
    old = a["s"].encode("utf-8")
    new = b.encode("utf-8") + b"\0"
    pos = pt4.find(old)
    assert pos >= 0, ("id4 no encontrado", a["s"][:60])
    slot = struct.unpack_from("<I", pt4, pos - 4)[0]
    assert len(new) <= slot, ("id4 no cabe", a["s"][:60], len(new), slot)
    assert all(v == 0 for v in pt4[pos + len(old):pos + slot]), a["s"][:60]
    pt4[pos:pos + slot] = new + b"\0" * (slot - len(new))
    n4 += 1
assert bytes(pt4) != orig4
put(4, bytes(pt4))

blob = build_ordered(SRC, new_files)
open(OUT, "wb").write(blob)
c2 = load(OUT)
for r in c2.rows:
    assert r["ex"] == len(c2.plain(r)), (r["id"], r["ex"], len(c2.plain(r)))
print("escrito", OUT, len(blob),
      "| id2", n2, "id4", n4,
      "| id1", sum(1 for a, b in zip(res_en, res_es) if a["id"] == 1),
      "| id3", sum(1 for a, b in zip(res_en, res_es) if a["id"] == 3),
      "| verificado")
