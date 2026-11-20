# -*- coding: utf-8 -*-
"""Comprueba si los residuales EN de SysText estan referenciados por tablas."""
import re
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/SysText.cpk"
c = load(P)
targets = [
    "Terrain Handling Up: Air", "Terrain Handling Up: Grd", "Terrain Handling Up: Wtr",
    "Emperor of Darkness", "Great General of Darkness",
    "Aestivalis Custom Hikaru Unit", "Calidus Multi-phase Beam Cannon",
    "High Energy Long-range Beam Cannon", "Kurogane Five Certain Death Attack",
    "ass to ass", "screw you", "the yeti",
]
for r in c.rows:
    try:
        pt = c.plain(r)
    except Exception:
        continue
    # offsets referenciados desde cualquier tabla de 4 bytes en la fila
    refs = set()
    for off in range(0, len(pt) - 3, 4):
        v = struct.unpack_from("<I", pt, off)[0]
        if v < len(pt):
            refs.add(v)
    for s in targets:
        b = s.encode("utf-8")
        pos = pt.find(b)
        if pos < 0:
            continue
        print("row", r["id"], repr(s[:40]), "pos", hex(pos), "referenciado", pos in refs)
