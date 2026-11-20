# -*- coding: utf-8 -*-
"""Reenvuelve el plain traducido (con acentos) dentro de un CPK valido.

El archivo output/OP_CK_es_real_null.cpk es el contenido descifrado de la
fila 0 con las traducciones aplicadas in-situ (mismo tamano). Se toma el
CPK original del backup como plantilla y se reconstruye el contenedor.
"""
import os
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

SRC = r"C:/Dev/Default Project/srwv/backup/OP_CK_original.cpk"
PLAIN = r"C:/Dev/Default Project/srwv/output/OP_CK_es_real_null.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/OP_CK_es_acc.cpk"

pt = open(PLAIN, "rb").read()
print("plain traducido:", len(pt), "bytes")

cf = load(SRC)
r0 = cf.rows[0]
print("fila 0: id", r0["id"], "ex", r0["ex"], "size", r0["size"])
assert len(pt) == r0["ex"], "el plain no coincide con ExtractSize"

for name in ("Akitó", "Ámuro", "Bánjo", "Tobía", "Capitán Gamillas",
             "Soldado del Imperio Júpiter", "Analizador"):
    print("  %-28s %s" % (name, "OK" if name.encode("utf-8") in pt else "NO"))

new_files = {r0["id"]: (cf.cipher(r0, pt), r0["ex"])}
out = build_ordered(SRC, new_files)
with open(OUT, "wb") as f:
    f.write(out)
print("escrito", OUT, len(out))

chk = load(OUT)
print("diag:", chk.cpk.diagnose() or "ok")
for r in chk.rows:
    p = chk.plain(r)
    print("fila", r["id"], "ex", r["ex"], "len", len(p), "igual", r["ex"] == len(p))
