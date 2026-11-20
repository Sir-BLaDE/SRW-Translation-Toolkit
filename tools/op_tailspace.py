# -*- coding: utf-8 -*-
"""Muestra el espacio de NULs disponible tras cada cadena de OP.CPK."""
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/BTLC/EN0/OP.CPK"
cf = load(P)
targets = ["AI", "Analyzer", "Gamillas Captain", "High Spec AI",
           "Jupiter Empire Soldier", "Martian Successor", "Neo Zeon Soldier",
           "Federation Soldier", "Wolfgang Subordinate", "Tenth Angel",
           "Metal Beast"]
for r in cf.rows:
    pt = cf.plain(r)
    print("==== FILA", r["id"])
    for t in targets:
        b = t.encode()
        start = 0
        while True:
            i = pt.find(b, start)
            if i < 0:
                break
            j = i + len(b)
            while j < len(pt) and pt[j] == 0:
                j += 1
            print("  %-24s off=%06x longitud=%2d NULs_tras=%2d espacio=%2d"
                  % (t, i, len(b), j - (i + len(b)) - 1, j - i))
            start = i + 1
