# -*- coding: utf-8 -*-
"""Escanear todos los CPK pequenos buscando 'press any button' en varias codificaciones."""
import os
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

G = r"D:/Juegos/-SPARROW-/Super Robot Wars V"
NEEDLES = {
    'ascii': b"Press any button",
    'ascii_lower': b"press any button",
    'utf16le': "Press any button".encode("utf-16le"),
    'utf16be': "Press any button".encode("utf-16be"),
}

count = 0
for root, dirs, files in os.walk(G):
    for f in files:
        if not f.lower().endswith('.cpk'):
            continue
        p = os.path.join(root, f)
        try:
            size = os.path.getsize(p)
        except Exception:
            continue
        if size > 25 * 1024 * 1024:
            continue
        count += 1
        try:
            cf = load(p)
        except Exception:
            continue
        for r in cf.rows:
            try:
                pt = cf.plain(r)
            except Exception:
                continue
            hits = [k for k, n in NEEDLES.items() if n in pt]
            if hits:
                rel = os.path.relpath(p, G)
                print("%s  id=%d  hits=%s  len=%d" % (rel, r['id'], ",".join(hits), len(pt)))

print("CPK escaneados:", count)
