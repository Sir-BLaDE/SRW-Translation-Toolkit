# -*- coding: utf-8 -*-
"""Dump hex/ascii de los primeros bytes de una fila."""
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

SRC = r"C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk"
NEW = r"C:/Dev/Default Project/srwv/outputs/Prologue_es.cpk"

for label, path, rid in [("ORIG", SRC, 1), ("ES", NEW, 1)]:
    cf = load(path)
    pt = cf.plain(next(r for r in cf.rows if r["id"] == rid))
    print("\n=== %s fila %d len=%d ===" % (label, rid, len(pt)))
    for base in range(0, 320, 16):
        chunk = pt[base:base+16]
        h = " ".join("%02x" % b for b in chunk)
        a = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        print("%04x  %-47s  %s" % (base, h, a))
