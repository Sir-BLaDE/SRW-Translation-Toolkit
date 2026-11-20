# -*- coding: utf-8 -*-\n"""Sonda rapida de CPK EN no traducidos: filas, tamano y cadenas ASCII visibles."""
import re
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

G = r"D:/Juegos/-SPARROW-/Super Robot Wars V/"
FILES = [
    "CommonData/MtData/EN/lega_zkn.cpk",
    "CommonData/MtData/EN/MtV_all_keyword_def.cpk",
    "CommonData/MtData/EN/rpw_jstr.cpk",
    "Data/DLCDIRE/BFL_EN.CPK",
    "Data/DLCDIRE/EN/dlc003_en.cpk",
    "Data/DLCDIRE/EN/dlc330_en.cpk",
    "Data/KURODATA/privacy_en_win.cpk",
]
RUN = re.compile(rb"[ -~]{6,}")


def sample(data, limit=12):
    out = []
    for m in RUN.finditer(data):
        s = m.group().decode("ascii", "replace")
        if re.search(r"[A-Za-z]{3}", s):
            out.append(s)
        if len(out) >= limit:
            break
    return out


for rel in FILES:
    p = G + rel
    try:
        c = load(p)
    except Exception as e:
        print("=== %s ERROR %s" % (rel, e))
        continue
    total = 0
    samples = []
    for f in c.rows:
        try:
            pt = c.plain(f)
        except Exception:
            continue
        total += len(pt)
        if len(samples) < 12:
            samples += sample(pt, 12 - len(samples))
    print("=== %s filas=%d plain=%d" % (rel, len(c.rows), total))
    for s in samples:
        print("    ", repr(s[:120]))
