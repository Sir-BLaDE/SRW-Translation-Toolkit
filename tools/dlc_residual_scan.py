# -*- coding: utf-8 -*-
"""Busca bloques [[...]] con ingles claro en los DLC reconstruidos."""
import glob
import io
import json
import os
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

OUT = r"C:/Dev/Default Project/srwv/outputs/dlc_es"
BLOCK = re.compile(r"\[\[(.*?)\]\]", re.S)
EN = re.compile(r"\b(the|and|you|your|that|this|with|have|from|they|what|"
                r"would|there|their|about|just|like|know|going|been|"
                r"because|before|after|when|will|were|was|are|not|but|"
                r"for|his|her|she|him|one|all|out|get|got|can|don't|"
                r"it's|I'm|we're|you're|attack|defeat|enemy|ally)\b", re.I)
ES = re.compile(r"[áéíóúñÁÉÍÓÚ¿¡]|cualquier|derrotad|escuadr|fase|punto", re.I)

res = []
for p in sorted(glob.glob(os.path.join(OUT, "dlc*.cpk"))):
    cf = load(p)
    for r in cf.rows:
        if r["id"] == 2:
            continue
        try:
            t = cf.plain(r).decode("utf-8")
        except Exception:
            continue
        for m in BLOCK.finditer(t):
            b = m.group(1)
            if EN.search(b) and not ES.search(b):
                res.append((os.path.basename(p), r["id"], b[:110]))

print("bloques con ingles claro:", len(res))
for f, i, b in res[:40]:
    print("  %s fila %d: %r" % (f, i, b))
