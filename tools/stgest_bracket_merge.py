# -*- coding: utf-8 -*-
"""Valida y fusiona las traducciones de bloques [[...]] de STGEST."""
import glob
import io
import json
import re

D = r"C:/Dev/Default Project/srwv/datos"
W = D + "/stgest_bracket_work"
EN = re.compile(
    r"\b(and|you|your|yours|this|that|these|those|with|for|from|attack|"
    r"defend|defense|power|level|item|skill|range|damage|hit|miss|turn|"
    r"phase|start|press|select|confirm|cancel|point|ability|weapon|"
    r"pilot|enemy|ally|allies|action|next|continue|are|was|will|"
    r"not|if|of|it|be|or|but|in|on|at|to|is|have|had|do|does|did|"
    r"what|when|where|who|why|how|now|out|up|down|left|right|open|close|save|"
    r"load|data|set|get|using|become|becomes|increase|decrease|effect|"
    r"effective|only|also|just|very|more|most|less|than|then|there|here|"
    r"their|them|his|its|our|we|they|she|three|four|five)\b",
    re.I)
WHITELIST = ("Joe the Ace", "Ple Two", "Unit-01")

src = json.load(io.open(D + "/stgest_bracket_en.json", encoding="utf-8"))
merged = {}
problems = []
outs = sorted(glob.glob(W + "/b_*_out.json"))
for out in outs:
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
        if k.count("\r") != v.count("\r") or k.count("\n") != v.count("\n"):
            problems.append((out, "saltos distintos", k[:60]))
        if k.count("　") != v.count("　"):
            problems.append((out, "U+3000 distinto", k[:60]))
        kt = re.findall(r"\$kwb|\$kwe|\$[nlrfFc]", k)
        vt = re.findall(r"\$kwb|\$kwe|\$[nlrfFc]", v)
        if kt != vt:
            problems.append((out, "tokens distintos", k[:60]))
        if "（" in k and "（" not in v:
            problems.append((out, "perdio parentesis", k[:60]))
        check = v
        for w in WHITELIST:
            check = check.replace(w, "")
        if EN.search(check):
            problems.append((out, "ingles residual", k[:60], v[:80]))
        merged[k] = v

missing = set(src) - set(merged)
if missing:
    problems.append(("global", "faltan", len(missing)))
print("salidas", len(outs), "fusionadas", len(merged), "de", len(src),
      "problemas", len(problems))
for p in problems[:30]:
    print("  ", p)
if not problems and len(merged) == len(src):
    dest = D + "/stgest_bracket_es.json"
    with io.open(dest, "w", encoding="utf-8") as fh:
        json.dump(merged, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("->", dest)

# Solapamiento con las otras pasadas de traduccion
quoted = json.load(io.open(D + "/stgest_quoted_es.json", encoding="utf-8"))
qkeys = set(quoted)
overlap_q = [k for k in merged if any(q in k for q in qkeys)]
overlap_dlg = [k for k in merged if "「" in k or "」" in k]
print("solape con cadenas citadas:", len(overlap_q),
      "| con dialogos:", len(overlap_dlg))
for k in overlap_q[:5]:
    print("  Q", repr(k[:90]))
