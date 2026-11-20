# -*- coding: utf-8 -*-
"""Extrae los bloques DSC2 en ingles pendientes de traducir.

Los campos DSC2 tienen un tamano fijo con relleno; el texto util termina en
la marca KANA. Se guarda un JSON por archivo con el texto exacto como clave.
"""
import io
import json
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

G = r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN"
D = r"C:/Dev/Default Project/srwv/datos"
FILES = ["MtZkn_Pt.cpk", "MtZkn_Rt.cpk", "MtZkn_Nm.cpk"]
WORDS = [
    " the ", " and ", " with ", " for ", " from ", " this ", " that ",
    " you ", " your ", " he ", " she ", " they ", " but ", " not ",
    " are ", " was ", " will ", " have ", " has ", " battle ", " pilot ",
    " mobile suit ", " attack ", " after ", " when ", " while ", " his ",
    " her ", " their ", " as ", " at ", " by ", " it ", " is ", " in ",
    " on ", " to ", " of ",
]

for name in FILES:
    c = load(G + "/" + name)
    vals = {}
    for f in c.rows:
        d = bytes(b ^ 0x5E for b in c.plain(f))
        i = d.find(b"DSC2")
        if i < 0:
            continue
        sz = struct.unpack_from("<H", d, i + 4)[0]
        blob = d[i + 6:i + 6 + sz]
        k = blob.find(b"KANA")
        txt = (blob[:k] if k >= 0 else blob).decode("utf-8", "replace")
        low = " " + txt.lower() + " "
        if any(w in low for w in WORDS):
            vals.setdefault(txt, []).append(f["id"])
    key = name.split("_")[1].split(".")[0].lower()
    out = D + "/mtzkn_" + key + "_dsc2_en.json"
    with io.open(out, "w", encoding="utf-8") as fh:
        json.dump({t: v for t, v in sorted(vals.items())}, fh,
                  ensure_ascii=False, indent=2)
        fh.write("\n")
    print(key, "unicos", len(vals), "ids", sum(len(v) for v in vals.values()),
          "chars", sum(len(t) for t in vals), "->", out)
