# -*- coding: utf-8 -*-
"""Comprueba cadenas entre comillas simples pendientes en STGEST."""
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/STAGE/STGEST_EN.CPK"
EN = re.compile(
    r"\b(the|and|you|your|this|that|with|for|from|attack|defend|defense|power|"
    r"level|item|skill|move|range|damage|hit|miss|turn|phase|start|press|select|"
    r"confirm|cancel|name|point|ability|weapon|pilot|unit|enemy|ally|allies|"
    r"action|end|next|continue|yes|are|was|will|not|can|if|of|it|be|or|but|in|"
    r"on|at|to|is|have|has|had|do|does|did|what|when|where|who|why|how|now|out|"
    r"up|down|left|right|open|close|save|load|data|set|get|use|using|become|"
    r"becomes|increase|decrease|effect|effective|only|also|just|very|more|most|"
    r"less|than|then|there|here|their|them|his|her|its|our|my|we|they|he|she|"
    r"one|two|three|four|five)\b", re.I)
SKIP = re.compile(r"^(pid_|Sc|SC_|V_|ENEMY_|EVENT_|/|\\|DEBUG_DATA|commondata|stage)")

c = load(P)
hits = {}
for f in c.rows:
    d = c.plain(f).decode("utf-8", "replace")
    for m in re.finditer(r"'([^'\r\n]{8,300})'", d):
        s = m.group(1)
        if EN.search(s) and not SKIP.match(s):
            hits.setdefault(s, []).append(f["id"])
print("single quoted", len(hits))
for k, v in list(hits.items())[:50]:
    print(v[:3], repr(k[:140]))
