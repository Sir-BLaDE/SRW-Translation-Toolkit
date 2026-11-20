# -*- coding: utf-8 -*-
"""Comparar byte a byte original vs version segura de Prologue."""
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

A = r"C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk"
B = r"C:/Dev/Default Project/srwv/outputs/Prologue_es_inplace_v7.cpk"

a = load(A)
b = load(B)

for r in a.rows:
    x = a.plain(r)
    y = b.plain(next(q for q in b.rows if q["id"] == r["id"]))
    assert len(x) == len(y)
    diffs = [i for i in range(len(x)) if x[i] != y[i]]
    if not diffs:
        continue
    # agrupar en rangos
    ranges = []
    s = p = diffs[0]
    for i in diffs[1:]:
        if i == p + 1:
            p = i
        else:
            ranges.append((s, p))
            s = p = i
    ranges.append((s, p))
    print("fila %-3d  bytes distintos=%-6d rangos=%d" % (r["id"], len(diffs), len(ranges)))
    for s, e in ranges[:3]:
        print("   @%d-%d  ORIG=%r  ES=%r" % (s, e, x[s:min(e+1, s+50)], y[s:min(e+1, s+50)]))
