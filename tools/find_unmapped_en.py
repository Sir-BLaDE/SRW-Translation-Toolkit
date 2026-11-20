# -*- coding: utf-8 -*-\n"""Busca cadenas inglesas del original que NO estan en el mapa de traduccion."""
import io
import json
import re
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

SRC, TM = sys.argv[1], sys.argv[2]
POOL, PEND = 0x48, 0x1EE10
cf = load(SRC)
pt = cf.plain(cf.rows[0])
trans = json.load(io.open(TM, encoding="utf-8"))
ES = re.compile(r"[áéíóúñÁÉÍÓÚ¿¡]|\b(el|la|los|las|de|del|que|y|con|por|para|no|es|son|un|una)\b", re.I)
EN = re.compile(r"\b(the|and|you|your|that|this|with|from|they|for|are|will|when|unit|units|weapon|weapons|damage|move|movement|turn|phase|start|all|by|to|of|in|on|at|is|be|it|its|as|or|an|a)\b", re.I)
pos = POOL
n = 0
while pos < PEND:
    end = pt.find(b"\0", pos)
    raw = pt[pos:end]
    try:
        s = raw.decode("utf-8")
    except Exception:
        pos = end + 1
        continue
    if s and s not in trans and EN.search(s) and not ES.search(s):
        n += 1
        print("OFF %06X %r" % (pos - POOL, s[:300]))
    pos = end + 1
print("TOTAL SIN MAPA:", n)
