# -*- coding: utf-8 -*-
"""Muestra fragmentos ingleses limpios de un CPK con id de fila."""
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = sys.argv[1]
PAT = re.compile(sys.argv[2], re.I)
SPLIT = re.compile(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]")
cf = load(P)
seen = set()
for r in cf.rows:
    pt = cf.plain(r)
    for part in SPLIT.split(pt):
        if len(part) < 8:
            continue
        try:
            s = part.decode("utf-8")
        except Exception:
            continue
        for line in re.split(r"\r\n|\n", s):
            line = line.strip("\u3000 \t\r")
            if PAT.search(line) and line not in seen:
                seen.add(line)
                print("fila %-4d %r" % (r["id"], line[:300]))
