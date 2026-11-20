# -*- coding: utf-8 -*-
"""Cuenta terminos preservados en ingles en todos los CPK principales."""
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
    G + r"/KURODATA/EN/KPACK_P4_RG_EN.CPK",
    G + r"/STAGE/STGEST_EN.CPK",
    CS + r"/LanguageData/EN/LT00_EN.cpk",
    CS + r"/LanguageData/EN/B_LT00_EN.cpk",
    CS + r"/../MtData/EN/MtZkn_Pt.cpk",
    CS + r"/../MtData/EN/MtZkn_Rt.cpk",
    CS + r"/../MtData/EN/MtZkn_Nm.cpk",
    CS + r"/../MtData/EN/rpw_jstr.cpk",
]
PAT = re.compile(
    r"\b(Newtypes?|mobile suits?|Mobile Suits?|"
    r"Captain|Federation Soldier|Super Soldier|"
    r"Martian Successors?|Jupiter Empire)\b", re.I)

for p in FILES:
    if not os.path.exists(p):
        continue
    cf = load(p)
    c = {}
    for r in cf.rows:
        try:
            t = cf.plain(r).decode("utf-8", "ignore")
        except Exception:
            continue
        for m in PAT.finditer(t):
            k = m.group(0)
            c[k] = c.get(k, 0) + 1
    if c:
        print("%-22s %s" % (os.path.basename(p),
              " ".join("%s=%d" % (k, v) for k, v in sorted(c.items()))))
