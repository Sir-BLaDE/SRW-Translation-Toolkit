# -*- coding: utf-8 -*-
"""Buscar 'Press any button' y terminos de menu en TODOS los CPK instalados."""
import os
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

G = r"D:/Juegos/-SPARROW-/Super Robot Wars V"
TARGETS = {
    "OP.CPK": G + r"/Data/BTLC/EN0/OP.CPK",
    "SysText": G + r"/Data/AIDDATA/EN/SysText.cpk",
    "LayoutImage": G + r"/Data/AIDDATA/EN/LayoutImage.cpk",
    "LayoutData": G + r"/Data/AIDDATA/EN/LayoutData.cpk",
    "Prologue": G + r"/Data/AIDDATA/EN/Prologue.cpk",
    "LT00": G + r"/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk",
    "B_LT00": G + r"/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk",
    "CMN00": G + r"/Data/BTLC/EN0/CMN00.CPK",
    "CMN00_PC": G + r"/Data/BTLC/EN0/CMN00_PC.CPK",
    "FontInfo": G + r"/Data/AIDDATA/EN/FontInfo.cpk",
}
TERMS = [b"Press any button", b"press any button", b"Settings", b"Continue",
         b"Load", b"Start", b"New Game", b"Quit", b"Language"]

for label, path in TARGETS.items():
    if not os.path.exists(path):
        print("%-14s NO EXISTE" % label)
        continue
    try:
        cf = load(path)
    except Exception as e:
        print("%-14s LOAD ERR %s" % (label, e))
        continue
    found = []
    for r in cf.rows:
        try:
            pt = cf.plain(r)
        except Exception:
            continue
        for t in TERMS:
            if t in pt:
                found.append((t.decode("ascii"), r["id"], pt.count(t)))
    if found:
        print("%-14s %s" % (label, ", ".join("%s(id%d x%d)" % x for x in found)))
