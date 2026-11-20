# -*- coding: utf-8 -*-
"""Lista las cadenas todavia en ingles en B_LT00_EN_es.cpk."""
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load as load_cpk
from lt00 import load as load_lt

P = r"C:/Dev/Default Project/srwv/outputs/B_LT00_EN_es.cpk"
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
    r"time|added|based|number|times|equivalent|skill|adjacent|original|dealt|destroy|"
    r"acquire|earn|total|bronze|silver|gold|emblem|stacked|stackable|exp|increase)\b",
    re.I,
)
ES = set("áéíóúñÁÉÍÓÚ¿¡")

c = load_cpk(P)
t = load_lt(c.plain(c.rows[0]))
uniq = list(dict.fromkeys(t.strings))
en = [s for s in uniq if s and ENW.search(s) and not any(x in ES for x in s)]
print("B_LT00 unicas", len(uniq), "EN restantes", len(en))
with open(r"C:/Dev/Default Project/srwv/datos/b_lt00_restante.txt", "w", encoding="utf-8") as fh:
    for s in en:
        fh.write(s + "\n")
for s in en[:60]:
    print(repr(s[:130]))
