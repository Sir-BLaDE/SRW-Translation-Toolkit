# -*- coding: utf-8 -*-
"""Busca el texto de 'press start' en bytes raw de todos los CPK del juego."""
import os
import re

G = r"D:/Juegos/-SPARROW-/Super Robot Wars V"
pats = []
for s in ("PRESS START", "PRESS ANY BUTTON", "PULSE START", "PULSA CUALQUIER", "PULSA START"):
    pats.append((s + " ascii", re.compile(s.encode("ascii"), re.I)))
    pats.append((s + " utf16", re.compile(s.encode("utf-16le"), re.I)))

hits = 0
for root, dirs, files in os.walk(G):
    for fn in files:
        if not fn.lower().endswith(".cpk"):
            continue
        p = os.path.join(root, fn)
        try:
            data = open(p, "rb").read()
        except Exception:
            continue
        for label, pat in pats:
            for m in pat.finditer(data):
                hits += 1
                print(label, p.replace(G + "\\", ""), hex(m.start()),
                      repr(data[max(0, m.start()-30):m.end()+30]))
print("hits", hits)
