# -*- coding: utf-8 -*-
"""Aplica terminos verificados de doblaje anime a los mapas activos.

Términos usados en doblajes españoles documentados:
  traje móvil / trajes móviles (Gundam Hathaway, ES)
  Nuevo Tipo / Nuevos Tipos (Gundam, ES)
  Sucesor Marciano / Sucesores Marcianos (Nadesico, ES)
  Capitán (ES)
Solo se tocan los VALORES; las claves son texto original inglés.
"""
import glob
import io
import json
import os
from collections import Counter

D = r"C:/Dev/Default Project/srwv/datos"

# Orden: frases largas primero.
REPL = [
    ("Artificial Newtype", "Nuevo Tipo artificial"),
    ("artificial Newtype", "Nuevo Tipo artificial"),
    ("Newtype Artificial", "Nuevo Tipo artificial"),
    ("Martian Successors", "Sucesores Marcianos"),
    ("Martian Successor", "Sucesor Marciano"),
    ("Federation Soldier", "Soldado de la Federación"),
    ("federation soldier", "Soldado de la Federación"),
    ("Jupiter Empire", "Imperio de Júpiter"),
    ("Jupiter War", "Guerra de Júpiter"),
    ("Mobile Suits", "Trajes móviles"),
    ("Mobile suits", "Trajes móviles"),
    ("mobile suits", "trajes móviles"),
    ("Mobile Suit", "Traje móvil"),
    ("Mobile suit", "Traje móvil"),
    ("mobile suit", "traje móvil"),
    ("Newtypes", "Nuevos Tipos"),
    ("newtypes", "Nuevos Tipos"),
    ("Newtype", "Nuevo Tipo"),
    ("newtype", "Nuevo Tipo"),
    ("Captain's", "del Capitán"),
    ("captain's", "del Capitán"),
    ("Captain", "Capitán"),
    ("captain", "Capitán"),
    ("Super Soldier", "Supersoldado"),
    ("super soldier", "Supersoldado"),
    ("Soldier", "Soldado"),
    ("soldier", "Soldado"),
]

FILES = [
    "systext_trans.json",
    "prologue_trans_v7.json",
    "kpack_rg_es.json",
    "ln_id0_es.json",
    "ln_id1_es.json",
    "ln_id3_compact_es.json",
    "ln_id4_es.json",
    "ln_residual_es_list.json",
    "es_tm.json",
    "rpw_jstr_es.json",
    "stgest_bracket_es.json",
    "stgest_quoted_es.json",
]
FILES += sorted(os.path.basename(p) for p in glob.glob(os.path.join(D, "b_lt00_rest_es_p*.json")))
FILES += sorted(os.path.basename(p) for p in glob.glob(os.path.join(D, "mtzkn_*_es*.json")))

def fix(s):
    if not isinstance(s, str):
        return s, 0
    out = s
    n = 0
    for a, b in REPL:
        c = out.count(a)
        if c:
            out = out.replace(a, b)
            n += c
    return out, n

def walk(o, counter):
    if isinstance(o, dict):
        for k, v in list(o.items()):
            nv, n = walk(v, counter)
            if n and isinstance(v, str):
                o[k] = nv
            counter[0] += n
        return o, 0
    if isinstance(o, list):
        for i, v in enumerate(o):
            nv, n = walk(v, counter)
            if n and isinstance(v, str):
                o[i] = nv
            counter[0] += n
        return o, 0
    return fix(o)

grand = Counter()
for name in FILES:
    p = os.path.join(D, name)
    if not os.path.exists(p):
        continue
    data = json.load(io.open(p, encoding="utf-8"))
    cnt = [0]
    walk(data, cnt)
    if cnt[0]:
        with io.open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print("%-38s %d" % (name, cnt[0]))
        grand[name] = cnt[0]
print("total cambios:", sum(grand.values()))
