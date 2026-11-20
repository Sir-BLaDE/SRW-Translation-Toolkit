# -*- coding: utf-8 -*-
"""Extrae cadenas entre comillas pendientes de traducir de STGEST."""
import io
import json
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"C:/Dev/Default Project/srwv/backup/STGEST_EN_original.cpk"
OUT = r"C:/Dev/Default Project/srwv/datos/stgest_quoted_en.json"
EN = re.compile(
    r"\b(the|and|you|your|yours|this|that|these|those|with|for|from|attack|"
    r"defend|defense|power|level|item|skill|move|range|damage|hit|miss|turn|"
    r"phase|start|press|select|confirm|cancel|name|point|ability|weapon|"
    r"pilot|unit|enemy|ally|allies|action|end|next|continue|yes|are|was|will|"
    r"not|can|if|of|it|be|or|but|in|on|at|to|is|have|has|had|do|does|did|"
    r"what|when|where|who|why|how|now|out|up|down|left|right|open|close|save|"
    r"load|data|set|get|use|using|become|becomes|increase|decrease|effect|"
    r"effective|only|also|just|very|more|most|less|than|then|there|here|"
    r"their|them|his|her|its|our|my|we|they|he|she|one|two|three|four|five)\b",
    re.I)
SKIP = re.compile(r"^(pid_|Sc|SC_|V_|ENEMY_|EVENT_|/|\\|DEBUG_DATA|commondata|stage)")

c = load(P)
vals = {}
for f in c.rows:
    d = c.plain(f).decode("utf-8", "replace")
    for m in re.finditer(r'"([^"\r\n]{8,300})"', d):
        s = m.group(1)
        if EN.search(s) and not SKIP.match(s):
            vals.setdefault(s, []).append(f["id"])

with io.open(OUT, "w", encoding="utf-8") as fh:
    json.dump({k: v for k, v in sorted(vals.items())}, fh,
              ensure_ascii=False, indent=2)
    fh.write("\n")
print("unicas", len(vals), "ocurrencias", sum(len(v) for v in vals.values()),
      "chars", sum(len(k) for k in vals), "->", OUT)
