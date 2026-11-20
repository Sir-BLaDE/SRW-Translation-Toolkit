# -*- coding: utf-8 -*-\n"""Vuelca filas con ingles real de un CPK para traducirlas."""
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = sys.argv[1]
PAT = re.compile(sys.argv[2], re.I)
cf = load(P)
for r in cf.rows:
    t = cf.plain(r).decode("utf-8", "ignore")
    if PAT.search(t):
        print("=" * 60)
        print("FILA", r["id"])
        print(repr(t))
