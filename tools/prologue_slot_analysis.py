# -*- coding: utf-8 -*-
"""Analizar huecos de strings en cada fila del Prologue original."""
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

SRC = r"C:/Dev/Default Project/srwv/backup/Prologue_original_20261118.cpk"
cf = load(SRC)

STR = re.compile(rb"[ -~]{5,}")

for r in cf.rows:
    pt = cf.plain(r)
    slots = []
    for m in STR.finditer(pt):
        s = m.group(0)
        # solo texto con letras, descartar ruido de ceros/bytes de control
        if not re.search(rb"[A-Za-z]{3}", s):
            continue
        j = m.end()
        while j < len(pt) and pt[j] == 0:
            j += 1
        free = j - m.end()
        slots.append((m.start(), s.decode("ascii", "replace"), len(s), free))
    if slots:
        print("\n=== fila %d (ex=%d) : %d strings ===" % (r["id"], r["ex"], len(slots)))
        for off, s, n, free in slots[:40]:
            print("  @%-7d len=%-4d libre=%-4d  %r" % (off, n, free, s[:110]))
        if len(slots) > 40:
            print("  ... (%d mas)" % (len(slots) - 40))
