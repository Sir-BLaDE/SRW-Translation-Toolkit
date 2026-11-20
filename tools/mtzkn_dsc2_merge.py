# -*- coding: utf-8 -*-
"""Valida y fusiona las traducciones DSC2 de los lotes."""
import glob
import io
import json
import os
import re

D = r"C:/Dev/Default Project/srwv/datos"
W = D + "/dsc2_work"
EN = re.compile(r"\b(and|with|for|from|this|that|you|your|they|but|not|are|was|will|have|has|pilot|attack|after|when|while|their)\b")
TAG = "<srw-tag=before-clear-text-here>"

for key in ["pt", "rt", "nm"]:
    src = json.load(io.open(D + "/mtzkn_" + key + "_dsc2_en.json", encoding="utf-8"))
    merged = {}
    problems = []
    outputs = sorted(glob.glob(W + "/" + key + "_*_out.json"))
    for out in outputs:
        got = json.load(io.open(out, encoding="utf-8"))
        if set(got) - set(src):
            problems.append((out, "claves sobrantes", len(set(got) - set(src))))
        for k, v in got.items():
            if k in merged:
                problems.append((out, "clave duplicada", k[:60]))
                continue
            if not isinstance(v, str):
                problems.append((out, "valor no str", k[:60]))
                continue
            if not v.startswith("^^"):
                problems.append((out, "sin ^^", k[:60]))
            if TAG in k and TAG not in v:
                problems.append((out, "perdio tag", k[:60]))
            if k.count("\n") != v.count("\n"):
                problems.append((out, "distintas saltos", k[:60]))
            if EN.search(v.replace(TAG, "")):
                problems.append((out, "ingles residual", k[:60], v[:80]))
            merged[k] = v
    missing = set(src) - set(merged)
    if missing:
        problems.append(("global", "faltan", len(missing)))
    print(key, "salidas", len(outputs), "fusionadas", len(merged),
          "de", len(src), "problemas", len(problems))
    for p in problems[:20]:
        print("  ", p)
    if not problems and len(merged) == len(src):
        dest = D + "/mtzkn_" + key + "_dsc2_es.json"
        with io.open(dest, "w", encoding="utf-8") as fh:
            json.dump(merged, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print("  ->", dest)
