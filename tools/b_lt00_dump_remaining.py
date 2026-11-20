# -*- coding: utf-8 -*-
"""Vuelca las cadenas pendientes de B_LT00 con su indice, en lotes."""
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

pend = []
for i, s in enumerate(t.strings):
    if s in done or not is_en(s):
        continue
    pend.append((i, s))

batch = int(sys.argv[1]) if len(sys.argv) > 1 else 0
start = batch * 100
chunk = pend[start:start + 100]
print("pendientes totales", len(pend), "lote", batch, "rango", start, "-", start + len(chunk))
for i, s in chunk:
    print("%5d\t%s" % (i, s.replace("\r", "\\r").replace("\n", "\\n")))
