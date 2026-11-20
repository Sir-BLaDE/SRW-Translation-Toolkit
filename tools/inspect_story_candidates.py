# -*- coding: utf-8 -*-
"""Comparar contenido de texto de CPK originales vs candidatos traducidos."""
import os
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

G = r"D:/Juegos/-SPARROW-/Super Robot Wars V"
O = r"C:/Dev/Default Project/srwv/outputs"

PAIRS = [
    ("Prologue", G + r"/Data/AIDDATA/EN/Prologue.cpk", O + r"/Prologue_es.cpk"),
    ("STGEST_EN", G + r"/Data/STAGE/STGEST_EN.CPK", O + r"/STGEST_EN_es.cpk"),
    ("SysText", G + r"/Data/AIDDATA/EN/SysText.cpk", O + r"/SysText_es_final.cpk"),
    ("LT00", G + r"/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk", O + r"/LT00_EN_es.cpk"),
    ("B_LT00", G + r"/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk", O + r"/B_LT00_EN_es.cpk"),
    ("CMN00_PC", G + r"/Data/BTLC/EN0/CMN00_PC.CPK", O + r"/CMN00_PC_es.cpk"),
]

# marcadores: palabras tipicas del texto de historia en ingles vs espanol
EN = [b"the ", b"you ", b"our ", b"will ", b"have ", b"This ", b"that ", b"with ",
      b"them ", b"their ", b"because ", b"attack ", b"mission ", b"enemy "]
ES_UTF8 = [w.encode("utf-8") for w in ["el ", "la ", "los ", "las ", "que ", "con ", "para ",
           "por ", "una ", "uno ", "nosotros", "usted", "atacar", "enemigo", "misión",
           "espera", "ahora", " Aspecto"]]
ACCENT = re.compile(rb"[\xc3\xa1\xc3\xa9\xc3\xad\xc3\xb3\xc3\xba\xc3\xb1\xc2\xbf\xc2\xa1]")


def blob(path):
    cf = load(path)
    return b"".join(cf.plain(r) for r in cf.rows)


def report(label, path):
    b = blob(path)
    en = {w.decode("ascii").strip(): b.count(w) for w in EN}
    es = sum(b.count(w) for w in ES_UTF8)
    acc = len(ACCENT.findall(b))
    print("  %-14s len=%-10d EN=%-5d ES=%-5d acentos=%d" %
          (label, len(b), sum(en.values()), es, acc))
    return b


for name, orig, new in PAIRS:
    print("\n=== %s ===" % name)
    if not os.path.exists(orig):
        print("  original no existe:", orig)
        continue
    if not os.path.exists(new):
        print("  candidato no existe:", new)
        continue
    a = report("ORIGINAL", orig)
    b = report("TRADUCIDO", new)
    # ejemplos de frases espanolas nuevas
    samples = []
    for m in re.finditer(rb"[ -~\xc2\xa1-\xc3\xbf]{16,}", b):
        s = m.group(0).decode("utf-8", "replace")
        if re.search(r"[áéíóúñ¿¡]", s) and len(s) < 200:
            samples.append(s)
        if len(samples) >= 4:
            break
    for s in samples:
        print("     ES:", repr(s[:150]))
