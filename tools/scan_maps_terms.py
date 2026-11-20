# -*- coding: utf-8 -*-
"""Cuenta terminos ingleses en los VALORES de todos los mapas JSON de datos/."""
import glob
import io
import json
import os
from collections import Counter

D = r"C:/Dev/Default Project/srwv/datos"
PAT = {
    "Newtype": ["Newtype", "Newtypes"],
    "mobile suit": ["mobile suit", "mobile suits", "Mobile Suit", "Mobile Suits"],
    "Captain": ["Captain", "captain"],
    "Martian": ["Martian Successor", "Martian Successors"],
    "Soldier": ["Federation Soldier", "Soldier"],
    "Innovator": ["Innovator"],
    "X-Rounder": ["X-Rounder"],
}

def walk(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield str(k)
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)

files = sorted(glob.glob(os.path.join(D, "*.json")))
files += sorted(glob.glob(os.path.join(D, "**", "*.json"), recursive=True))
files = sorted(set(files))
tot = Counter()
for p in files:
    try:
        data = json.load(io.open(p, encoding="utf-8"))
    except Exception:
        continue
    c = Counter()
    for s in walk(data):
        for label, terms in PAT.items():
            for t in terms:
                n = s.count(t)
                if n:
                    c[label] += n
    if c:
        rel = os.path.relpath(p, D)
        print("%-55s %s" % (rel, " ".join("%s=%d" % (k, v) for k, v in sorted(c.items()))))
        tot.update(c)
print("\nTOTALES:", " ".join("%s=%d" % (k, v) for k, v in sorted(tot.items())))
