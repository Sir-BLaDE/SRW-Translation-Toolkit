# -*- coding: utf-8 -*-
"""Busca restos de ingles no detectados por dlc_batch_check en los lotes ES."""
import glob
import io
import json
import os
import re
from collections import Counter

BATCH = r"C:/Dev/Default Project/srwv/datos/dlc_work/batches"

# Palabras inglesas que NO estan en el checker y suelen colarse en el cuerpo.
PAT = re.compile(
    r"\b(Martian Successors?|Jupiter Empire|Jupiter War|Super Soldiers?|"
    r"Space Pirates?|Federation Soldiers?|Earth Federation|"
    r"Supreme Leader|Dark Side|Light Side|Galaxy Empire|"
    r"Blue Cosmos|Crossbone Vanguard|Zanscare Empire|"
    r"Spirit Commands?|Support (?:Attack|Defense)|"
    r"Mobile Suits?|mobile suits?|Aces?|Ace Pilot|"
    r"Newtypes?|Innovators?|Coordinators?|"
    r"Defeat|Victory|Enemy|Allies|Mission|Scenario|Stage|"
    r"Hit Points|HP|EN|Will Power|Morale|"
    r"Pilot|Weapon|Shield|Booster|Armour|Armor|"
    r"Attack|Move|Range|Map|Weapon|Turn|Phase)\b",
    re.I,
)

# Se permiten ciertos terminos conservados por el glosario.
ALLOW = re.compile(
    r"\b(Newtype|Innovator|mobile suit|I-Field|Psycommu|Funnel|"
    r"Reflector Bit|Gundam Hammer|AMBAC|Vernier|Trans-Am|X-Rounder|"
    r"Crossbone Vanguard|Blue Cosmos|HP|EN|Jupiter|Gundam|Nadesico|"
    r"Yamato|Gamillas|Grungust|Huckebein|Mazinger|Getter Robo)\b",
    re.I,
)

counts = Counter()
where = {}
for p in sorted(glob.glob(os.path.join(BATCH, "*.es.json"))):
    try:
        arr = json.load(io.open(p, encoding="utf-8"))
    except Exception:
        continue
    for i, s in enumerate(arr):
        for m in PAT.finditer(s):
            term = m.group(0)
            if ALLOW.fullmatch(term):
                continue
            counts[term] += 1
            where.setdefault(term, []).append((os.path.basename(p), i, s[:120]))

for term, n in counts.most_common():
    print("%-24s %3d" % (term, n))
    for f, i, s in where[term][:6]:
        print("    %s[%d] %r" % (f, i, s))
if not counts:
    print("sin restos")
