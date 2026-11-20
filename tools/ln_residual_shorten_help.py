# -*- coding: utf-8 -*-\n"""Muestra cuantos bytes hay que recortar en cada traduccion que no cabe."""
import io
import json
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

D = r"C:/Dev/Default Project/srwv/datos"
P = r"C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_full_stable.cpk"
en = json.load(io.open(D + "/ln_residual_en.json", encoding="utf-8"))
es = json.load(io.open(D + "/ln_residual_es_list.json", encoding="utf-8"))
c = load(P)
pt2 = c.plain([x for x in c.rows if x["id"] == 2][0])
pt4 = c.plain([x for x in c.rows if x["id"] == 4][0])


def align(v, a):
    return (v + a - 1) & ~(a - 1)


for i, (a, b) in enumerate(zip(en, es)):
    need = len(b.encode("utf-8")) + 1
    if a["id"] == 2:
        p = pt2.find(a["s"].encode("utf-8"))
        slot = align(len(a["s"].encode("utf-8")) + 1, 4)
    else:
        p = pt4.find(a["s"].encode("utf-8"))
        slot = struct.unpack_from("<I", pt4, p - 4)[0]
    if need > slot:
        print("=" * 70)
        print("IDX", i, "fila", a["id"], "slot", slot,
              "bytes", need, "recortar", need - slot)
        print("EN:", repr(a["s"]))
        print("ES:", repr(b))
