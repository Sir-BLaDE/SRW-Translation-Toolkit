# -*- coding: utf-8 -*-
"""Divide las cadenas citadas de STGEST en lotes."""
import io
import json
import os

D = r"C:/Dev/Default Project/srwv/datos"
W = D + "/stgest_work"
os.makedirs(W, exist_ok=True)
SIZE = 40
src = json.load(io.open(D + "/stgest_quoted_en.json", encoding="utf-8"))
items = list(src.items())
for n, start in enumerate(range(0, len(items), SIZE), 1):
    chunk = dict(items[start:start + SIZE])
    out = W + "/q_%02d_in.json" % n
    with io.open(out, "w", encoding="utf-8") as fh:
        json.dump(chunk, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(out, len(chunk), sum(len(k) for k in chunk))
