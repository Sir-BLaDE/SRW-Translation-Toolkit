# -*- coding: utf-8 -*-
"""Comprueba que las traducciones residuales caben en sus campos reales.

id2: huecos alineados a 4 = align4(len(texto EN)+1).
id4: todo texto lleva un u32 de longitud en pos-4 ( tanto en registros parse4
     como en los compact 'scen' ).
"""
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
assert len(en) == len(es), (len(en), len(es))

c = load(P)
pt2 = c.plain([x for x in c.rows if x["id"] == 2][0])
pt4 = c.plain([x for x in c.rows if x["id"] == 4][0])


def align(v, a):
    return (v + a - 1) & ~(a - 1)


bad = []
for i, (a, b) in enumerate(zip(en, es)):
    s, t = a["s"], b
    need = len(t.encode("utf-8")) + 1
    if a["id"] == 2:
        p = pt2.find(s.encode("utf-8"))
        if p < 0:
            bad.append((i, 2, "NO ENCONTRADO", s[:50]))
            continue
        slot = align(len(s.encode("utf-8")) + 1, 4)
        if need > slot:
            bad.append((i, 2, "NO CABE %d>%d" % (need, slot), t[:60]))
    elif a["id"] == 4:
        p = pt4.find(s.encode("utf-8"))
        if p < 0:
            bad.append((i, 4, "NO ENCONTRADO", s[:50]))
            continue
        slot = struct.unpack_from("<I", pt4, p - 4)[0]
        if need > slot:
            bad.append((i, 4, "NO CABE %d>%d" % (need, slot), t[:60]))

print("total", len(en), "problemas", len(bad))
for x in bad:
    print("  ", x)
