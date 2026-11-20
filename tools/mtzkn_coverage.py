# -*- coding: utf-8 -*-
"""Comprueba cobertura de los mapas MTZKN frente a las descripciones instaladas."""
import io
import json
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

G = r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN"
D = r"C:/Dev/Default Project/srwv/datos"
FILES = {
    "NM": (G + "/MtZkn_Nm.cpk", D + "/mtzkn_nm_es_accent.json"),
    "PT": (G + "/MtZkn_Pt.cpk", D + "/mtzkn_pt_es_accent.json"),
    "RT": (G + "/MtZkn_Rt.cpk", D + "/mtzkn_rt_es_accent.json"),
}
ES = set("áéíóúñÁÉÍÓÚ¿¡")
ENW = re.compile(r"\b(the|you|your|this|that|these|those|and|with|for|from|attack|defend|defense|power|level|item|skill|move|range|damage|hit|miss|turn|phase|start|press|select|confirm|cancel|name|point|ability|weapon|pilot|unit|enemy|ally|allies|action|end|next|continue|yes|are|was|will|not|can|if|of|it|be|or|but|in|on|at|to|is|have|has|had|do|does|did|what|when|where|who|why|how|now|out|up|down|left|right|open|close|save|load|data|set|get|use|using|become|becomes|increase|decrease|effect|effective|only|also|just|very|more|most|less|than|then|there|here|their|them|his|her|its|our|my|we|they|he|she|one|two|three|four|five|year|old|rank|member|former|after|during|battle|final|learns|finds|becomes|takes|works|sent|joins|returns|meets|fights|death|killed|destroyed|built|developed|created|known|called|based|version|model|type|system|forces|force|army|navy|organization|group|team|school|high|middle|first|second|third|fourth|fifth|time|times|same|other|another|both|each|every|many|much|some|any|all|never|always|only|even|still|yet|already|also|again|once|since|until|while|before|because|though|although|however|therefore|thus|so|such|than|then)\b", re.I)

for key, (p, tm) in FILES.items():
    c = load(p)
    T = json.load(io.open(tm, encoding="utf-8"))
    descs = []
    for f in c.rows:
        pt = c.plain(f)
        dec = bytes(b ^ 0x5E for b in pt)
        try:
            s = dec.decode("utf-8")
        except Exception:
            continue
        descs.append((f["id"], s))
    en_full = [(fid, s) for fid, s in descs if ENW.search(s) and not any(c2 in ES for c2 in s)]
    covered = sum(s in T for fid, s in en_full)
    print("%s: rows=%d map=%d EN-full=%d cubiertas=%d faltan=%d" %
          (key, len(descs), len(T), len(en_full), covered, len(en_full) - covered))
