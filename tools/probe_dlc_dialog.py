# -*- coding: utf-8 -*-\n"""Extrae literales de cadena (con escapes) de las filas de dialogo DLC."""
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

G = r"D:/Juegos/-SPARROW-/Super Robot Wars V/"
c = load(G + "Data/DLCDIRE/EN/dlc003_en.cpk")
LIT = re.compile(rb'"((?:[^"\\]|\\.){8,})"')
for fid in (1, 2, 3, 4):
    pt = c.plain([x for x in c.rows if x["id"] == fid][0])
    print("=== fila", fid, "len", len(pt))
    n = 0
    for m in LIT.finditer(pt):
        raw = m.group(1)
        try:
            t = raw.decode("utf-8")
        except Exception:
            continue
        if not re.search(r"[A-Za-z]{3}", t):
            continue
        if t.startswith(("/", "C:", "c:", "F:", "f:", "rid_", "pid_", "bgm_")):
            continue
        n += 1
        if n <= 25:
            print("   ", repr(t[:120]))
    print("   literales de texto:", n)
