# -*- coding: utf-8 -*-
"""Busca 'press any button' en bytes crudos de todos los archivos del juego."""
import os

G = r"D:/Juegos/-SPARROW-/Super Robot Wars V"
PATS = {
    'ascii': b"Press any button",
    'ascii_lower': b"press any button",
    'utf16le': "Press any button".encode('utf-16le'),
    'utf16be': "Press any button".encode('utf-16be'),
    'ascii_upper': b"PRESS ANY BUTTON",
}

n = 0
for root, dirs, files in os.walk(G):
    for f in files:
        p = os.path.join(root, f)
        try:
            if os.path.getsize(p) > 40 * 1024 * 1024:
                continue
        except Exception:
            continue
        n += 1
        try:
            data = open(p, 'rb').read()
        except Exception:
            continue
        hits = [k for k, v in PATS.items() if v in data]
        if hits:
            print(os.path.relpath(p, G), "->", ",".join(hits))
print("archivos revisados:", n)
