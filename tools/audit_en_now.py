# -*- coding: utf-8 -*-
"""Auditoria exhaustiva de ingles residual en TODOS los CPK traducidos.

Explora filas UTF-8, bloques [[...]], cadenas NT, BLTU de CMN00 y variantes
XOR de MtZkn. Clasifica como EN si hay palabras inglesas claras y no hay
marcadores espanoles.
"""
import glob
import os
import re
import sys
from collections import Counter, OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cpk_util import load as load_cpk
from srwv_bltu import load as load_bltu

G = os.path.expanduser('~/mnt/Super Robot Wars V/Data')
CS = os.path.expanduser('~/mnt/Super Robot Wars V/CommonData/ShiroData')
FILES = OrderedDict([
    ("PROLOGUE", G + r"/AIDDATA/EN/Prologue.cpk"),
    ("SYSTEXT", G + r"/AIDDATA/EN/SysText.cpk"),
    ("CMN00", G + r"/BTLC/EN0/CMN00.CPK"),
    ("KPACK_LN", G + r"/KURODATA/EN/KPACK_P4_LN_EN.CPK"),
    ("KPACK_RG", G + r"/KURODATA/EN/KPACK_P4_RG_EN.CPK"),
    ("STGEST", G + r"/STAGE/STGEST_EN.CPK"),
    ("LT00", CS + r"/LanguageData/EN/LT00_EN.cpk"),
    ("B_LT00", CS + r"/LanguageData/EN/B_LT00_EN.cpk"),
    ("MTZKN_PT", os.path.expanduser("~/mnt/Super Robot Wars V/CommonData/MtData/EN/MtZkn_Pt.cpk")),
    ("MTZKN_RT", os.path.expanduser("~/mnt/Super Robot Wars V/CommonData/MtData/EN/MtZkn_Rt.cpk")),
    ("MTZKN_NM", os.path.expanduser("~/mnt/Super Robot Wars V/CommonData/MtData/EN/MtZkn_Nm.cpk")),
    ("RPW_JSTR", os.path.expanduser("~/mnt/Super Robot Wars V/CommonData/MtData/EN/rpw_jstr.cpk")),
])
for _p in sorted(glob.glob(G + r"/DLCDIRE/EN/dlc*.cpk")):
    FILES["DLC_" + os.path.basename(_p)[4:7].upper()] = _p

EN = re.compile(
    r"\b(the|and|you|your|yours|that|this|these|those|with|have|has|from|"
    r"they|them|their|what|would|there|about|just|like|know|going|been|"
    r"because|before|after|when|will|were|was|are|not|but|for|his|her|"
    r"she|him|one|all|out|get|got|can|don't|it's|i'm|we're|you're|"
    r"attack|defeat|defeated|enemy|allies|ally|weapon|damage|level|"
    r"turn|phase|start|press|select|confirm|cancel|continue|yes|no|"
    r"move|range|hit|miss|point|ability|skill|unit|pilot|mission|"
    r"commander|captain|soldier|officer|successor|empire|king|queen|"
    r"where|who|why|how|need|want|should|could|would|must|shall|"
    r"receive|receive|receive|increase|decrease|effective|only|also|"
    r"just|very|more|most|less|than|then|here|its|our|my|me|we|they|"
    r"he|she|it|be|is|do|does|did|of|in|on|at|to|by|or|an|a)\b", re.I)
ES = re.compile(r"[áéíóúñÁÉÍÓÚ¿¡]|"
                r"\b(el|la|los|las|un|una|de|del|al|que|es|son|en|y|con|"
                r"por|para|no|sí|su|sus|este|esta|más|pero|como|cuando|"
                r"donde|porque|nada|todo|también|puede|puedes|hay|hasta|"
                r"desde|entre|sobre|bajo|muy|mucho|poco|ahora|aquí|así|"
                r"bien|mal|me|te|se|nos|os|les|lo|le|sido|ser|era|fue|"
                r"tan|tanto|ella|él|nosotros|usted|tu|tus|nuestro)\b", re.I)
# Nombres propios / terminos conservados que no son ingles a traducir.
KEEP = re.compile(
    r"\b(Gundam|Zaminger|Mazinger|Getter|Nadesico|Yamato|Gamillas|"
    r"Grungust|Huckebein|Amuro|Char|Kamille|Banagher|Newtype|"
    r"mobile suit|I-Field|Psycommu|Funnel|Reflector Bit|AMBAC|Vernier|"
    r"Trans-Am|Innovator|X-Rounder|Crossbone Vanguard|Celestial Being|"
    r"Neo Zeon|Earth Federation|Jupiter|Mars|Nadesico)\b", re.I)
SPLIT = re.compile(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def strings_from(data, xor=0):
    if xor:
        data = bytes(b ^ xor for b in data)
    out = []
    for part in SPLIT.split(data):
        if len(part) < 5:
            continue
        try:
            s = part.decode("utf-8")
        except Exception:
            continue
        for line in re.split(r"\r\n|\n", s):
            line = line.strip("\u3000 \t\r")
            if len(line) < 5:
                continue
            out.append(line)
    return out


def is_en(s):
    if ES.search(s):
        return False
    m = EN.search(s)
    if not m:
        return False
    if KEEP.search(s):
        # si solo hay terminos conservados + ingles, puede ser nombre oficial
        rest = EN.sub(" ", s)
        if not EN.search(rest):
            return False
    return True


report = OrderedDict()
for name, path in FILES.items():
    if not os.path.exists(path):
        continue
    try:
        cf = load_cpk(path)
    except Exception as e:
        print("ERROR carga", name, e)
        continue
    pool = Counter()
    for r in cf.rows:
        pt = cf.plain(r)
        for s in strings_from(pt):
            if is_en(s):
                pool[s] += 1
        for s in strings_from(pt, 0x5E):
            if is_en(s):
                pool[s] += 1
        if name == "CMN00":
            try:
                t = load_bltu(pt)
                for x in t.all_strings():
                    s = x[3] if isinstance(x, (tuple, list)) else str(x)
                    if isinstance(s, str) and is_en(s):
                        pool[s] += 1
            except Exception:
                pass
    report[name] = pool

out = os.path.expanduser("~/mnt/srwv/datos/audit_en_now.txt")
with open(out, "w", encoding="utf-8") as f:
    for name, pool in report.items():
        f.write("\n" + "=" * 70 + "\n")
        f.write("%s: %d cadenas EN\n" % (name, len(pool)))
        for s, n in pool.most_common():
            f.write("  %3d  %r\n" % (n, s[:150]))

print("%-12s %8s %8s" % ("CPK", "EN_UNIQ", "EN_TOT"))
for name, pool in report.items():
    print("%-12s %8d %8d" % (name, len(pool), sum(pool.values())))
print("\ndetalle ->", out)
