"""lt00_diff.py - descomprime LT00 y compara contenidos."""
import sys
from cpk_util import load
from crilayla import maybe_decompress

paths = [
    "D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk",
    "D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk",
    "C:/Dev/Default Project/srwv/backup/LT00_EN_instalado_antes.cpk",
    "C:/Dev/Default Project/srwv/backup/LT00_EN_modificado_roto.cpk",
    "D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/JP/LT00_JP.cpk",
]

for p in paths:
    cf = load(p)
    print("=" * 70)
    print(p.split("/")[-1], "| entradas", len(cf.rows))
    for f in cf.rows:
        raw = cf.raw(f)
        try:
            dec = maybe_decompress(raw)
            ok = "OK" if f["ex"] == len(dec) or len(dec) >= f["ex"] else "TAMANO RARO"
        except Exception as e:
            dec = b""
            ok = "ERROR %s" % e
        print("  id %d: almacenado %d B, ex=%d, descomprimido %d B -> %s" % (
            f["id"], len(raw), f["ex"], len(dec), ok))
        txt = dec
        # imprimir cadenas legibles
        cur = ""
        found = []
        for b in txt:
            c = chr(b)
            if 32 <= b < 127 or c in "\r\n":
                cur += c
            else:
                if len(cur) >= 4:
                    found.append(cur)
                cur = ""
        if len(cur) >= 4:
            found.append(cur)
        print("    cadenas legibles: %d" % len(found))
        for s in found[:6]:
            print("      %r" % s[:80])
