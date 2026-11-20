# -*- coding: utf-8 -*-
"""Lista los prefijos de hablante y terminos preservados en los lotes EN."""
import glob
import io
import json
import os
import re
from collections import Counter

BATCH = r"C:/Dev/Default Project/srwv/datos/dlc_work/batches"

pref = Counter()
terms = Counter()
for p in sorted(glob.glob(os.path.join(BATCH, "batch_*.json"))):
    if p.endswith(".es.json"):
        continue
    try:
        arr = json.load(io.open(p, encoding="utf-8"))
    except Exception:
        continue
    for s in arr:
        m = re.search(r"([「（])", s)
        if m:
            head = s[:m.start()]
            name = head.split("\r\n")[0].split("\n")[0]
            pref[name] += 1
        for t in re.findall(r"\b(?:mobile suits?|Newtypes?|Captain|"
                            r"Federation Soldiers?|Super Soldiers?|"
                            r"Martian Successors?|Jupiter Empire|Jupiter War|"
                            r"Space Pirates?|Commander|Lieutenant|Sergeant|"
                            r"Doctor|Professor|General|Admiral|Major|"
                            r"Operator|Pilot|Soldier|Officer|Knight|"
                            r"Supreme Leader|Vanguard|Empire|Federation)\b",
                            s, re.I):
            terms[t] += 1

print("=== PREFIJOS UNICOS (%d) ===" % len(pref))
for k, n in pref.most_common():
    print("%5d  %r" % (n, k))
print("\n=== TERMINOS (%d) ===" % len(terms))
for k, n in terms.most_common():
    print("%5d  %r" % (n, k))
