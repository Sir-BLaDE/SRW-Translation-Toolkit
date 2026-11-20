# -*- coding: utf-8 -*-
"""Comprueba si los residuales EN de un CPK estan referenciados por tablas."""
import re
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

G = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data"
CS = r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData"
FILES = {
    "PROLOGUE": G + r"/AIDDATA/EN/Prologue.cpk",
    "SYSTEXT": G + r"/AIDDATA/EN/SysText.cpk",
    "CMN00": G + r"/BTLC/EN0/CMN00.CPK",
    "KPACK_LN": G + r"/KURODATA/EN/KPACK_P4_LN_EN.CPK",
    "MTZKN_NM": CS + r"/../MtData/EN/MtZkn_Nm.cpk",
    "MTZKN_PT": CS + r"/../MtData/EN/MtZkn_Pt.cpk",
    "MTZKN_RT": CS + r"/../MtData/EN/MtZkn_Rt.cpk",
}

ES_CHARS = set("áéíóúñÁÉÍÓÚ¿¡")
ES_WORDS = re.compile(r"\b(el|la|los|las|un|una|unos|unas|de|del|al|que|es|son|en|y|con|por|para|no|sí|si|su|sus|este|esta|estos|estas|más|pero|como|cuando|donde|porque|nada|todo|todos|tambien|también|puede|puedes|hay|hasta|desde|entre|sobre|bajo|ante|tras|muy|mucho|poco|ahora|aqui|aquí|asi|así|bien|mal|me|te|se|nos|os|les|lo|le|du|da|do|sido|ser|era|fue|tan|tanto|ella|él|ello|nosotros|usted|ustedes|mi|mis|tu|tus|nuestro|nuestra|vue|vuestro)\b", re.I)
EN_WORDS = re.compile(r"\b(the|you|your|yours|this|that|these|those|and|with|for|from|attack|defend|defense|power|level|item|skill|move|range|damage|hit|miss|turn|phase|start|press|select|confirm|cancel|name|point|ability|weapon|pilot|unit|enemy|ally|allies|action|end|next|continue|yes|are|was|will|not|can|if|of|it|be|or|but|in|on|at|to|is|have|has|had|do|does|did|what|when|where|who|why|how|now|out|up|down|left|right|open|close|save|load|data|set|get|use|using|become|becomes|increase|decrease|effect|effective|only|also|just|very|more|most|less|than|then|there|here|their|them|his|her|its|our|my|we|they|he|she|one|two|three|four|five)\b", re.I)


def strings_from(data, xor=0):
    out = []
    if xor:
        data = bytes(b ^ xor for b in data)
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


def classify(s):
    es = bool(ES_WORDS.search(s)) or any(c in ES_CHARS for c in s)
    en = bool(EN_WORDS.search(s))
    if es and not en:
        return "ES"
    if en and not es:
        return "EN"
    if es and en:
        return "MIXTO"
    return "NEUTRO"


name = sys.argv[1]
c = load(FILES[name])
targets = set()
for r in c.rows:
    try:
        pt = c.plain(r)
    except Exception:
        continue
    pool = set(strings_from(pt))
    if name.startswith("MTZKN"):
        pool |= set(strings_from(pt, 0x5E))
    targets |= {s for s in pool if classify(s) == "EN"}

print("%s EN targets: %d" % (name, len(targets)))
nref = nor = 0
for r in c.rows:
    try:
        pt = c.plain(r)
    except Exception:
        continue
    refs = set()
    for off in range(0, len(pt) - 3, 4):
        v = struct.unpack_from("<I", pt, off)[0]
        if v < len(pt):
            refs.add(v)
    for s in sorted(targets):
        b = s.encode("utf-8")
        pos = pt.find(b)
        if pos < 0:
            continue
        if pos in refs:
            nref += 1
        else:
            nor += 1
        print("id=%-3s ref=%-5s pos=%-8s %s" % (r["id"], pos in refs, hex(pos), repr(s[:60])))
print("referenciados", nref, "no referenciados", nor)
