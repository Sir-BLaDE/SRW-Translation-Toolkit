# -*- coding: utf-8 -*-
"""Muestra el contexto de los terminos preservados en los CPK indicados."""
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

FILES = [
    r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk",
    r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk",
    r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/rpw_jstr.cpk",
]
PAT = re.compile(r"\b(Newtypes?|mobile suits?|Mobile Suits?|"
                 r"Captain|Martian Successor)\b", re.I)

for p in FILES:
    cf = load(p)
    print("\n===", p.split("/")[-1], "===")
    seen = set()
    for r in cf.rows:
        try:
            t = cf.plain(r).decode("utf-8", "ignore")
        except Exception:
            continue
        for m in PAT.finditer(t):
            ctx = t[max(0, m.start() - 70):m.end() + 70].replace("\r\n", "|").replace("\n", "|")
            if ctx in seen:
                continue
            seen.add(ctx)
            print("  fila %d [%s]: %r" % (r["id"], m.group(0), ctx))
            if len(seen) >= 30:
                break
        if len(seen) >= 30:
            break
