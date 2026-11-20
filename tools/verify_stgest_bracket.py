# -*- coding: utf-8 -*-
"""Verifica el CPK de STGEST reconstruido con la pasada de corchetes."""
import hashlib
import io
import json
import os
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

ORIG = r"C:/Dev/Default Project/srwv/backup/STGEST_EN_original.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/STGEST_EN_es.cpk"
INST = r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/STAGE/STGEST_EN.CPK"
D = r"C:/Dev/Default Project/srwv/datos"

co, cn = load(ORIG), load(OUT)
bad = []
for f in cn.rows:
    try:
        p = cn.plain(f)
    except Exception as e:
        bad.append((f["id"], "DECOMP", str(e)))
        continue
    if len(p) != f["ex"]:
        bad.append((f["id"], "EX", len(p), f["ex"]))
print("filas", len(cn.rows), "ex_mismatch", len(bad))
for b in bad[:10]:
    print("  ", b)

r594 = [r for r in cn.rows if r["id"] == 594][0]
p594 = cn.plain(r594)
print("fila594 ex", r594["ex"], "len(plain)", len(p594),
      "u16_ok", r594["ex"] <= 0xFFFF)

br = json.load(io.open(D + "/stgest_bracket_es.json", encoding="utf-8"))
orig_all = b"".join(co.plain(f) for f in co.rows)
new_all = b"".join(cn.plain(f) for f in cn.rows)
print("bloques [[ en original", orig_all.count(b"[["),
      "| en salida", new_all.count(b"[["))
res = 0
for en in br:
    if (("[[" + en + "]]").encode("utf-8")) in new_all:
        res += 1
print("bloques EN que sobreviven:", res)


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


print("md5 salida ", md5(OUT))
print("md5 instalado", md5(INST) if os.path.exists(INST) else "NO EXISTE")
