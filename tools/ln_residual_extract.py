# -*- coding: utf-8 -*-
"""Extrae los residuales EN de KPACK LN con su fila y contexto."""
import io
import json
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK"
ES_CHARS = set("áéíóúñÁÉÍÓÚ¿¡")
ES_WORDS = re.compile(r"\b(el|la|los|las|un|una|de|del|al|que|es|son|en|y|con|por|para|no|sí|su|sus|este|esta|más|pero|como|cuando|donde|porque|nada|todo|también|puede|hay|hasta|desde|entre|sobre|bajo|muy|mucho|ahora|aquí|así|bien|mal|me|te|se|nos|les|lo|le|sido|ser|era|fue|tan|ella|él|nosotros|usted|mi|mis|tu|tus|nuestro|nuestra)\b", re.I)
EN_WORDS = re.compile(r"\b(the|you|your|this|that|these|those|and|with|for|from|attack|defend|defense|power|level|item|skill|move|range|damage|hit|miss|turn|phase|start|press|select|confirm|cancel|name|point|ability|weapon|pilot|unit|enemy|ally|allies|action|end|next|continue|yes|are|was|will|not|can|if|of|it|be|or|but|in|on|at|to|is|have|has|had|do|does|did|what|when|where|who|why|how|now|out|up|down|left|right|open|close|save|load|data|set|get|use|using|become|increases|decrease|effect|only|also|just|very|more|most|less|than|then|there|here|their|them|his|her|its|our|my|we|they|he|she|one|two|three|four|five)\b", re.I)


def classify(s):
    es = bool(ES_WORDS.search(s)) or any(c in ES_CHARS for c in s)
    en = bool(EN_WORDS.search(s))
    return ("ES" if es and not en else "EN" if en and not es
            else "MIXTO" if es and en else "NEUTRO")


def strings_from(data):
    out = []
    for part in re.split(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", data):
        if len(part) < 4:
            continue
        try:
            s = part.decode("utf-8")
        except Exception:
            continue
        s = "".join(ch if (ch.isprintable() or ch in "\n\r\t　") else " " for ch in s).strip()
        if len(s) >= 4:
            out.append(s)
    return out


c = load(P)
rows = []
for f in c.rows:
    pt = c.plain(f)
    for s in strings_from(pt):
        if classify(s) == "EN":
            rows.append({"id": f["id"], "s": s})
rows.sort(key=lambda x: (x["id"], x["s"]))
with io.open(r"C:/Dev/Default Project/srwv/datos/ln_residual_en.json", "w", encoding="utf-8") as fh:
    json.dump(rows, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("residuales", len(rows))
for r in rows:
    print(r["id"], repr(r["s"][:120]))
