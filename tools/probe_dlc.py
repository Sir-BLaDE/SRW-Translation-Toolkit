# -*- coding: utf-8 -*-\n"""Inspecciona las filas de un CPK DLC y la tabla rpw_jstr."""
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

G = r"D:/Juegos/-SPARROW-/Super Robot Wars V/"
c = load(G + "Data/DLCDIRE/EN/dlc003_en.cpk")
print("filas", len(c.rows))
for f in c.rows:
    pt = c.plain(f)
    print("--- fila", f["id"], "len", len(pt), "head", repr(pt[:80]))
    # lineas con texto entre comillas
    txts = re.findall(rb'"([^"\\\r\n]{6,})"', pt)
    for t in txts[:6]:
        print("     str", repr(t[:100]))

print()
print("=== rpw_jstr ===")
c2 = load(G + "CommonData/MtData/EN/rpw_jstr.cpk")
pt = c2.plain(c2.rows[0])
print("len", len(pt), "head", repr(pt[:200]))
# imprimir cadenas legibles largas
for m in re.finditer(rb"[ -~]{10,}", pt):
    s = m.group().decode("ascii", "replace")
    if re.search(r"[A-Za-z]{4}", s):
        print("   ", repr(s[:110]))
