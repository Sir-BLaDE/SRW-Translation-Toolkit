# -*- coding: utf-8 -*-
"""Analiza que mapas existentes pueden aplicarse a B_LT00."""
import csv
import io
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from lt00 import load as lt

D = r"C:/Dev/Default Project/srwv/datos"
G = r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/"

ENW = re.compile(
    r"\b(the|you|your|this|that|these|and|with|for|from|attack|defend|power|level|"
    r"item|skill|move|range|damage|hit|miss|turn|phase|start|press|select|confirm|"
    r"cancel|name|point|ability|weapon|pilot|unit|enemy|ally|allies|action|end|next|"
    r"continue|yes|are|was|will|not|can|if|of|it|be|or|but|in|on|at|to|is|have|has|"
    r"do|does|what|when|where|who|how|now|out|up|down|left|right|open|close|save|load|"
    r"data|set|get|use|using|become|increase|decrease|effect|only|also|just|very|more|"
    r"most|less|than|then|there|here|their|them|his|her|its|our|my|we|they|he|she|"
    r"one|two|three|recover|receives?|gains?|amount|each|maximum|when|lands|critical|"
    r"cleared|per|during|battle|map|all|any|target|takes|until|after|before|first|"
    r"time|amount|start|turn)\b",
    re.I,
)

c = load(G + "B_LT00_EN.cpk")
t = lt(c.plain(c.rows[0]))
print("B_LT00 strings:", t.count, "unicas:", len(dict.fromkeys(t.strings)))

rows = list(csv.DictReader(io.open(D + "/lt00_pendientes.csv", encoding="utf-8", newline="")))
idxmap = {}
textmap = {}
for r in rows:
    en, es = r["en"], r["actual"]
    if en != es and es.strip():
        idxmap[int(r["idx"])] = es
        textmap[en] = es
print("pendientes: filas", len(rows), "idx traducidos", len(idxmap), "textos traducidos", len(textmap))

# ¿coinciden los indices?
idx_hit = sum(1 for i, s in enumerate(t.strings) if idxmap.get(i) == s)
text_en_hit = sum(1 for i, s in enumerate(t.strings) if s in textmap)
print("idx donde el texto actual ya es la traduccion:", idx_hit)
print("ocurrencias donde el texto original esta en el mapa:", text_en_hit)

long_en = [(i, s) for i, s in enumerate(t.strings) if len(s) > 25 and " " in s and ENW.search(s)]
print("cadenas largas EN:", len(long_en))
print("  cubiertas por indice:", sum(i in idxmap for i, s in long_en))
print("  cubiertas por texto:", sum(s in textmap for i, s in long_en))
print("  ya traducidas (no EN):", sum(s not in textmap and not ENW.search(s) for i, s in long_en))
print()
print("--- primeras largas EN no cubiertas ---")
n = 0
for i, s in long_en:
    if i in idxmap or s in textmap:
        continue
    print(i, repr(s[:130]))
    n += 1
    if n >= 30:
        break
