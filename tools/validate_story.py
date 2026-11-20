# -*- coding: utf-8 -*-
"""Validar CPK de historia: magic, load() y ExtractSize por fila."""
import os
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

CANDIDATES = [
    r"C:/Dev/Default Project/srwv/outputs/Prologue_es.cpk",
    r"C:/Dev/Default Project/srwv/outputs/STGEST_EN_es.cpk",
]

for p in CANDIDATES:
    print("\n===", os.path.basename(p), "===")
    with open(p, "rb") as f:
        head = f.read(4)
    print("  tamaño:", os.path.getsize(p), "magic:", repr(head))
    assert head == b"CPK ", "magic invalido"
    cf = load(p)
    print("  filas:", len(cf.rows), "diag:", cf.cpk.diagnose() or "ok")
    ok = True
    for r in cf.rows:
        pt = cf.plain(r)
        same = (r["ex"] == len(pt))
        ok &= same
        if len(cf.rows) <= 10 or not same:
            print("   id=%-3d ex=%-10d len=%-10d igual=%s" % (r["id"], r["ex"], len(pt), same))
    print("  RESULTADO:", "VALIDO" if ok else "INVALIDO")
