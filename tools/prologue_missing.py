# -*- coding: utf-8 -*-
"""Lista las partes de Prologue que siguen sin traduccion."""
import json
import io
import re

D = r"C:/Dev/Default Project/srwv/datos"
d = json.load(io.open(D + "/prologue_full_v2.json", encoding="utf-8"))
T = json.load(io.open(D + "/prologue_trans_v7.json", encoding="utf-8"))
ES = set("áéíóúñÁÉÍÓÚ¿¡")
ENW = re.compile(r"\b(the|you|your|this|that|and|with|for|from|of|in|on|at|to|is|are|was|were|will|be|by|as|an|a|it|its|with|support|graphics|director|senior|vice|president|coordinator|studio|fonts|provided|part|all rights reserved|trademark|powered|character|cut-in|original|art|production|unit|ltd|inc|corporation|music|sound|design|program|planner|writer|artist|animation|works|company|english|version|movie|the|edition|vs|and|the)\b", re.I)

missing = {}
for rid, rd in d.items():
    for si, row in enumerate(rd["rows"]):
        for part in row["parts"]:
            k = part.strip()
            if not k:
                continue
            es = T.get(k, "")
            if es.strip() and es != k:
                continue
            if not ENW.search(k) and not any(c in ES for c in k):
                continue
            missing[k] = (rid, si)

print("partes sin traducir:", len(missing))
for k, (rid, si) in sorted(missing.items(), key=lambda x: (int(x[1][0]), x[1][1])):
    print("fila %-3s slot %-4d %s" % (rid, si, repr(k[:120])))
