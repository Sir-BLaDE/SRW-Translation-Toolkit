# -*- coding: utf-8 -*-
import glob
import io
import json
import os
import sys

needle = sys.argv[1]
for p in sorted(glob.glob(r"C:/Dev/Default Project/srwv/datos/dlc_work/batches/*.json")):
    if p.endswith(".es.json"):
        continue
    try:
        arr = json.load(io.open(p, encoding="utf-8"))
    except Exception:
        continue
    for i, s in enumerate(arr):
        if needle.lower() in s.lower():
            es = p.replace(".json", ".es.json")
            trad = ""
            if os.path.exists(es):
                try:
                    trad = json.load(io.open(es, encoding="utf-8"))[i]
                except Exception:
                    trad = "<pendiente>"
            print("%s[%d]\n  EN %r\n  ES %r" % (os.path.basename(p), i, s, trad))
