# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

needles = [b"Beginner's Mode", b"Standard Mode", b"Guidance Mode",
           b"Protagonist Settings", b"First Name", b"Nickname",
           b"Blood-Type", b"Blood Type", b"Reading switching",
           b"End-Settings", b"End Settings", b"Reading Switching"]

files = {
    "LT00": r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk",
    "B_LT00": r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk",
    "LayoutData": r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/LayoutData.cpk",
    "SysText": r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/SysText.cpk",
    "LayoutImage": r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/LayoutImage.cpk",
}

for name, p in files.items():
    c = load(p)
    blob = b"".join(c.plain(r) for r in c.rows)
    hits = []
    for n in needles:
        i = blob.find(n)
        if i >= 0:
            hits.append((n.decode(), i))
    if hits:
        print(name, hits)
    else:
        print(name, "sin hits")
