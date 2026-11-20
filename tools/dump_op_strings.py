# -*- coding: utf-8 -*-
"""Extrae cadenas ASCII de OP.CPK fila 0 con desplazamiento."""
import re
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK"
cf = load(P)
pt = cf.plain(cf.rows[0])
seen = {}
for m in re.finditer(rb"[ -~]{3,}", pt):
    s = m.group().decode("ascii")
    # Solo mostrar strings de texto legible (con al menos 2 letras o espacio)
    if not re.search(r"[A-Za-z ]{2,}", s):
        continue
    seen.setdefault(s, []).append(m.start())
for s, offs in sorted(seen.items()):
    print("%6d  %r" % (len(offs), s[:120]))
