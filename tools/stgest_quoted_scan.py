# -*- coding: utf-8 -*-
"""Busca cadenas entre comillas con palabras inglesas en STGEST."""
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/STAGE/STGEST_EN.CPK"
EN = re.compile(
    r"\b(the|and|you|your|this|that|with|for|from|attack|defend|power|level|"
    r"item|skill|move|range|damage|hit|miss|turn|phase|start|press|select|"
    r"confirm|cancel|name|point|ability|weapon|pilot|unit|enemy|ally|allies|"
    r"action|end|next|continue|yes|are|was|will|not|can|if|of|it|be|or|but|"
    r"in|on|at|to|is|have|has|had|do|does|did|what|when|where|who|why|how|"
    r"now|out|up|down|left|right|open|close|save|load|data|set|get|use|using|"
    r"become|becomes|increase|decrease|effect|effective|only|also|just|very|"
    r"more|most|less|than|then|there|here|their|them|his|her|its|our|my|we|"
    r"they|he|she|one|two|three|four|five)\b", re.I)
SKIP = re.compile(r"^(pid_|Sc|SC_|V_|ENEMY_|EVENT_|/|\\|DEBUG_DATA|commondata|stage)")

c = load(P)
hits = []
for f in c.rows:
    d = c.plain(f).decode("utf-8", "replace")
    for m in re.finditer(r'"([^"\r\n]{8,200})"', d):
        s = m.group(1)
        if EN.search(s) and not SKIP.match(s):
            hits.append((f["id"], s))
print("hits", len(hits))
for a in hits[:120]:
    print(a)
