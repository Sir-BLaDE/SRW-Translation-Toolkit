# -*- coding: utf-8 -*-
"""Busca terminos del glosario que NO se tradujeron en los lotes de DLC.

Los terminos conservados a proposito (Newtype, mobile suit, I-Field, ...) se
ignoran. Los demas deben aparecer en espanol; si aparecen en ingles se avisa.
"""
import glob
import io
import json
import os
import re
from collections import Counter

BATCH = r"C:/Dev/Default Project/srwv/datos/dlc_work/batches"

# EN -> ES. Solo los que deben traducirse siempre.
MUST = {
    "ExC": "Cuenta Extra",
    "SP": "PE",
    "Tac Pts": "Pts Tác",
    "Focus": "Enfoque",
    "Great Ace": "Gran As",
    "Skill Programs": "Programas de Habilidad",
    "Boost Dash": "Impulso Veloz",
    "Smash Hit": "Golpe Demoledor",
    "Direct Attack": "Ataque Directo",
    "Multi Action": "Multiacción",
    "Lecture Board": "Panel de Clases",
    "Key Help": "Ayuda de Teclas",
    "Combat Record": "Registro de Combate",
    "End Phase": "Fin de Fase",
    "Spirit Commands": "Espíritus",
    "Targeting": "Puntería",
    "Armor": "Blindaje",
    "Custom Bonus": "Bonificación de Personalización",
    "Ace Bonus": "Bonificación de As",
    "Extra Action System": "Sistema de Acción Extra",
    "Distortion Field": "Campo de Distorsión",
    "Support Attack": "Ataque de Apoyo",
    "Support Defense": "Defensa de Apoyo",
}

pat = re.compile(r"\b(?:" + "|".join(re.escape(k) for k in MUST) + r")\b")
counts = Counter()
examples = {}
for p in sorted(glob.glob(os.path.join(BATCH, "*.es.json"))):
    arr = json.load(io.open(p, encoding="utf-8"))
    for i, s in enumerate(arr):
        for m in pat.finditer(s):
            term = m.group(0)
            counts[term] += 1
            examples.setdefault(term, (os.path.basename(p), i, s[:90]))

if counts:
    print("terminos de glosario aun en ingles:")
    for term, n in counts.most_common():
        f, i, ex = examples[term]
        print("  %-20s %3d  %s[%d] %r  (debe ser %r)" %
              (term, n, f, i, ex, MUST[term]))
else:
    print("glosario OK: ningun termino obligatorio quedo en ingles")
