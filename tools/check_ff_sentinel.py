# -*- coding: utf-8 -*-
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
    ca, cb = x.count(b"\xff\xff"), y.count(b"\xff\xff")
    if ca != cb:
        print("fila %-3d ff ff: orig=%d es=%d" % (r["id"], ca, cb))
        for i in range(len(x) - 1):
            if x[i:i+2] == b"\xff\xff":
                print("   @%d orig=%r es=%r" % (i, x[i:i+2], y[i:i+2]))
                break
