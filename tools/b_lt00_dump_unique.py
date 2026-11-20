# -*- coding: utf-8 -*-
"""Vuelca las cadenas inglesas UNICAS pendientes de B_LT00."""
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

uniq = []
seen = set()
for s in t.strings:
    if s in done or s in seen or not is_en(s):
        continue
    seen.add(s)
    uniq.append(s)

print("unicas pendientes:", len(uniq))
for n, s in enumerate(uniq):
    print("%4d\t%s" % (n, s.replace("\r", "\\r").replace("\n", "\\n")))
