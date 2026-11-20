# -*- coding: utf-8 -*-
"""Busca textos de pulsa start en CPK descomprimidos."""
import os
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

G = r"D:/Juegos/-SPARROW-/Super Robot Wars V"
CANDIDATES = [
    "Data/AIDDATA/COMMON/ButtonHintsSTEAM.cpk",
    "Data/AIDDATA/COMMON/ButtonHintsPC.cpk",
    "Data/AIDDATA/EN/FontInfo.cpk",
    "Data/AIDDATA/EN/LayoutData.cpk",
    "Data/AIDDATA/EN/LayoutImage.cpk",
    "Data/AIDDATA/COMMON/PrologueImage.cpk",
    "Data/AIDDATA/EN/Prologue.cpk",
    "Data/AIDDATA/EN/SysText.cpk",
    "Data/KURODATA/CMN/KPACK_PC_CMN.cpk",
]
PAT = re.compile(rb"(press\s+any\s+button|press\s+start|pulse\s+start|pulsa\s+cualquier|any\s+button)", re.I)

for rel in CANDIDATES:
    p = G + "/" + rel
    if not os.path.exists(p):
        continue
    try:
        c = load(p)
    except Exception as e:
        print(rel, "LOAD ERR", e)
        continue
    hits = []
    for f in c.rows:
        try:
            d = c.plain(f)
        except Exception as e:
            continue
        for m in PAT.finditer(d):
            hits.append((f["id"], m.group(0).decode("ascii", "replace"),
                         d[max(0, m.start()-40):m.end()+40]))
    print(rel, "filas", len(c.rows), "hits", len(hits))
    for fid, txt, ctx in hits[:5]:
        print("  id", fid, txt, repr(ctx[:120]))
