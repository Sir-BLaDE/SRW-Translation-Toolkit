# -*- coding: utf-8 -*-
"""Busca restos de nombres ingleses en todos los CPK instalados traducidos."""
import glob
import os
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

G = r"D:/Juegos/-SPARROW-/Super Robot Wars V"
CS = G + r"/CommonData/ShiroData"
FILES = [
    G + r"/AIDDATA/EN/SysText.cpk",
    G + r"/AIDDATA/EN/Prologue.cpk",
    G + r"/BTLC/EN0/CMN00.CPK",
    G + r"/KURODATA/EN/KPACK_P4_LN_EN.CPK",
    G + r"/STAGE/STGEST_EN.CPK",
    CS + r"/LanguageData/EN/LT00_EN.cpk",
    CS + r"/LanguageData/EN/B_LT00_EN.cpk",
    CS + r"/../MtData/EN/MtZkn_Pt.cpk",
    CS + r"/../MtData/EN/MtZkn_Rt.cpk",
    CS + r"/../MtData/EN/MtZkn_Nm.cpk",
    CS + r"/../MtData/EN/rpw_jstr.cpk",
]
FILES += sorted(glob.glob(G + r"/DLCDIRE/EN/dlc*.cpk"))

PAT = re.compile(
    r"(Martian Successors?|Jupiter Empire|Jupiter War|"
    r"Federation Soldier|Super Soldier|Soldiers? of Jupiter|"
    r"Martian Successor Nadesico|Jupiter\b)",
    re.I,
)

for p in FILES:
    if not os.path.exists(p):
        continue
    try:
        cf = load(p)
    except Exception as e:
        print("ERROR", p, e)
        continue
    hits = {}
    for r in cf.rows:
        try:
            t = cf.plain(r).decode("utf-8", "ignore")
        except Exception:
            continue
        for m in PAT.finditer(t):
            ctx = t[max(0, m.start() - 30):m.end() + 45].replace("\r\n", "|")
            hits.setdefault(m.group(0), []).append((r["id"], ctx))
    if hits:
        print("\n" + os.path.basename(p))
        for k, v in sorted(hits.items()):
            print("  %-28s %4d  ej: fila %d %r" % (k, len(v), v[0][0], v[0][1][:90]))
