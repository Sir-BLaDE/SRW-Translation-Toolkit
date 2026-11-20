# -*- coding: utf-8 -*-
"""Divide los JSON de DSC2 en lotes para traduccion."""
import io
import json
import os

D = r"C:/Dev/Default Project/srwv/datos"
W = D + "/dsc2_work"
os.makedirs(W, exist_ok=True)
SIZE = 20

for key in ["pt", "rt", "nm"]:
    src = json.load(io.open(D + "/mtzkn_" + key + "_dsc2_en.json", encoding="utf-8"))
    items = list(src.items())
    n = 0
    for start in range(0, len(items), SIZE):
        n += 1
        chunk = dict(items[start:start + SIZE])
        out = W + "/" + key + "_" + ("%02d" % n) + "_in.json"
        with io.open(out, "w", encoding="utf-8") as fh:
            json.dump(chunk, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print(out, len(chunk), sum(len(t) for t in chunk))
