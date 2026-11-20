# -*- coding: utf-8 -*-
"""Comparar estructura de filas de Prologue original vs candidato traducido."""
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

A = r"C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk"
B = r"C:/Dev/Default Project/srwv/outputs/Prologue_es.cpk"

for label, path in [("ORIGINAL", A), ("TRADUCIDO", B)]:
    cf = load(path)
    print("\n===", label, "===")
    print("filas:", len(cf.rows), "diag:", cf.cpk.diagnose() or "ok")
    for r in cf.rows:
        pt = cf.plain(r)
        keys = sorted(k for k in r.keys() if k not in ("data", "plain"))
        print(" id=%-3d ex=%-8d size=%-8d len=%-8d %s" % (
            r["id"], r["ex"], r["size"], len(pt),
            " ".join("%s=%s" % (k, r[k]) for k in keys if k in ("id", "ex", "size", "crc", "enc", "comp", "flag", "offset", "name"))))
