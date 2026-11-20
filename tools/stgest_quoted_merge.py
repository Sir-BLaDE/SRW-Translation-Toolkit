# -*- coding: utf-8 -*-
"""Valida y fusiona las traducciones de cadenas citadas de STGEST."""
import glob
import io
import json
import re

D = r"C:/Dev/Default Project/srwv/datos"
EN = re.compile(r"\b(the|and|with|for|from|this|that|you|your|attack|pilot|enemy|ally|allies|action|continue|phase|press|select|confirm|cancel|damage|weapon|skill|ability|range|miss|turn|start|next|not|will|are|was|were|but|if|of|it|be|or|in|on|at|to|is|what|when|where|why|how|now|out|up|down|left|right|open|close|save|load|data|set|get|using|become|increase|decrease|effect|only|also|just|very|more|most|less|than|then|there|their|them|his|her|its|our|my|we|they|he|she|one|two|three|four|five)\b", re.I)

src = json.load(io.open(D + "/stgest_quoted_en.json", encoding="utf-8"))
merged = {}
problems = []
for out in sorted(glob.glob(D + "/stgest_work/q_*_out.json")):
    got = json.load(io.open(out, encoding="utf-8"))
    for k, v in got.items():
        if k not in src:
            problems.append((out, "sobrante", k[:60]))
            continue
        if k in merged:
            problems.append((out, "duplicado", k[:60]))
            continue
        if not isinstance(v, str):
            problems.append((out, "no str", k[:60]))
            continue
        if k.count("\\n") != v.count("\\n"):
            problems.append((out, "distintos \\n", k[:60]))
        if EN.search(v):
            problems.append((out, "ingles residual", k[:60], v[:80]))
        merged[k] = v
missing = set(src) - set(merged)
if missing:
    problems.append(("global", "faltan", len(missing)))
print("fusionadas", len(merged), "de", len(src), "problemas", len(problems))
for p in problems[:30]:
    print("  ", p)
if not problems and len(merged) == len(src):
    dest = D + "/stgest_quoted_es.json"
    with io.open(dest, "w", encoding="utf-8") as fh:
        json.dump(merged, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("->", dest)
