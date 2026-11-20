# -*- coding: utf-8 -*-
"""Comparar terminos UI entre LayoutData original y traducido."""
import os
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

ORIG = r"C:/Dev/Default Project/srwv/backup/LayoutData_original.cpk"
ES = r"C:/Dev/Default Project/srwv/outputs/LayoutData_es.cpk"

TERMS = [b"Settings", b"Continue", b"Start", b"Select", b"Options",
         b"Beginner", b"Standard Mode", b"Guidance", b"First Name",
         b"Nickname", b"Blood Type", b"End Settings", b"Load"]


def blob(path):
    cf = load(path)
    return b"".join(cf.plain(r) for r in cf.rows)


a = blob(ORIG)
b = blob(ES)
print("original:", len(a), "traducido:", len(b))
print("\n%-18s %8s %8s" % ("TERMINO", "ORIG", "ES"))
for t in TERMS:
    print("%-18s %8d %8d" % (t.decode(), a.count(t), b.count(t)))

# Mostrar contexto de los terminos que quedan en el traducido
print("\n=== Contexto de terminos residuales en LayoutData_es ===")
for t in TERMS:
    pos = 0
    shown = 0
    while shown < 2:
        i = b.find(t, pos)
        if i < 0:
            break
        ctx = b[max(0, i-40):i+len(t)+40]
        txt = re.sub(rb"[^\x20-\x7e]", b".", ctx).decode("ascii", "replace")
        print("  %-16s @%d: ...%s..." % (t.decode(), i, txt))
        pos = i + 1
        shown += 1

# Mostrar ejemplos de texto espanol nuevo
print("\n=== Ejemplos de texto espanol en LayoutData_es ===")
for m in list(re.finditer(rb"[ -~\xc3\xa1\xc3\xe9\xc3\xad\xc3\xb3\xc3\xba\xc3\xb1]{12,}", b))[:30]:
    s = m.group(0).decode("utf-8", "replace")
    if re.search(r"[áéíóúñ¿¡]", s, re.I):
        print("  ", repr(s[:100]))
