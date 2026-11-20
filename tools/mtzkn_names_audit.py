# -*- coding: utf-8 -*-
"""Lista campos etiquetados (RBTN/RBN2/PRDC/CHNN/PLTN...) aun en ingles en MTZKN."""
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

BASE = r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/"
ES = set("áéíóúñÁÉÍÓÚ¿¡")
EN_W = re.compile(
    r"\b(the|of|and|in|on|for|with|from|to|type|mark|model|version|unit|attack|"
    r"new|great|super|dark|emperor|general|mobile|suit|gundam|class|edition|"
    r"movie|vs|unit|prototype|strike|force|space|beam|high|low|long|short)\b", re.I)
TAGS = (b"RBTN", b"RBN2", b"PRDC", b"CHFN", b"CHNN", b"PLTN", b"VOIC")

for fn in ("MtZkn_Rt.cpk", "MtZkn_Pt.cpk", "MtZkn_Nm.cpk"):
    c = load(BASE + fn)
    found = {}
    for f in c.rows:
        d = bytes(b ^ 0x5E for b in c.plain(f))
        for tag in TAGS:
            pos = 0
            while True:
                i = d.find(tag, pos)
                if i < 0:
                    break
                pos = i + len(tag)
                if pos >= len(d):
                    break
                n = d[pos]
                start = pos + 4
                if d[pos + 1:pos + 4] != b"^^^" or start + n > len(d):
                    continue
                try:
                    s = d[start:start + n].decode("utf-8")
                except Exception:
                    continue
                if len(s) < 4 or any(ch in ES for ch in s):
                    continue
                if not EN_W.search(s):
                    continue
                found.setdefault((tag.decode(), s), 0)
                found[(tag.decode(), s)] += 1
    print("===", fn, "campos EN unicos", len(found))
    bytag = {}
    for (tag, s), n in found.items():
        bytag.setdefault(tag, []).append((s, n))
    for tag in sorted(bytag):
        print("  --", tag, len(bytag[tag]))
        for s, n in sorted(bytag[tag])[:40]:
            print("     ", repr(s[:85]), "x", n)
