# -*- coding: utf-8 -*-\n"""Muestra los huecos reales de las descripciones id2 y los prefijos id4."""
import io
import json
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

D = r"C:/Dev/Default Project/srwv/datos"
P = r"C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_full_stable.cpk"
en = json.load(io.open(D + "/ln_residual_en.json", encoding="utf-8"))
c = load(P)
pt2 = c.plain([x for x in c.rows if x["id"] == 2][0])
pt4 = c.plain([x for x in c.rows if x["id"] == 4][0])

print("=== id2: descripciones que no caben ===")
bad2 = [i for i, x in enumerate(en) if x["id"] == 2]
#Fitcheck said these indices: 10..32 subset; recompute all
for i in bad2:
    s = en[i]["s"]
    b = s.encode("utf-8")
    pos = pt2.find(b)
    if pos < 0:
        continue
    end = pt2.find(b"\0", pos)
    nulls = 0
    j = end
    while j < len(pt2) and pt2[j] == 0:
        nulls += 1
        j += 1
    print(i, "pos", hex(pos), "lenEN", len(b), "hastaNUL", end - pos,
          "nulos", nulls, "| next", repr(pt2[j:j + 24]))

print()
print("=== id4: prefijo u32 de los compact scen ===")
bad4 = [i for i, x in enumerate(en) if x["id"] == 4]
for i in bad4:
    s = en[i]["s"]
    b = s.encode("utf-8")
    pos = pt4.find(b)
    if pos < 0:
        print(i, "NO ESTA", repr(s))
        continue
    pre = struct.unpack_from("<I", pt4, pos - 4)[0]
    nul = pt4.find(b"\0", pos)
    print(i, "pos", hex(pos), "pre", pre, "len", len(b),
          "hastaNUL", nul - pos, "|", repr(s))
