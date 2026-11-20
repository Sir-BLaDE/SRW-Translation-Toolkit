# -*- coding: utf-8 -*-
"""Vuelca TODAS las cadenas pendientes de B_LT00 (con vecinos para contexto)."""
import json
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load as load_cpk
from lt00 import load as load_lt
from b_lt00_classify import is_en

P = r"C:/Dev/Default Project/srwv/outputs/B_LT00_EN_es.cpk"
DONE = r"C:/Dev/Default Project/srwv/datos/b_lt00_rest_es.json"

c = load_cpk(P)
t = load_lt(c.plain(c.rows[0]))
done = {}
try:
    with open(DONE, encoding="utf-8") as fh:
        done = json.load(fh)
except FileNotFoundError:
    pass

idx = [i for i, s in enumerate(t.strings) if s not in done and is_en(s)]
print("pendientes:", len(idx))
for i in idx:
    lo = max(0, i - 1)
    hi = min(len(t.strings), i + 2)
    ctx = " | ".join("%d:%s" % (j, t.strings[j].replace("\r", "\\r").replace("\n", "\\n")[:70])
                     for j in range(lo, hi))
    print("%5d\t%s\t@@%s" % (i, t.strings[i].replace("\r", "\\r").replace("\n", "\\n"), ctx))
