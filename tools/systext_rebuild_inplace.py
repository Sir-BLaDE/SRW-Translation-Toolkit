# -*- coding: utf-8 -*-
"""Reconstruye SysText fila 2 SIN desplazar tablas: escribe cada traduccion
en su hueco original y, si no cabe, la coloca en un pool al final de la fila.

Así se conservan las posiciones absolutas de la tabla1 (0x1440), la tabla2
(0x1640) y todos los valores del cabecera.
"""
import json
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

ORIG = r"C:/Dev/Default Project/srwv/backup/SysText_antes_es.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/SysText_es_inplace.cpk"
ITEMS = r"C:/Dev/Default Project/srwv/datos/systext_row2.json"
TRANS = r"C:/Dev/Default Project/srwv/datos/systext_trans.json"
BASE = 0x30
TAB1 = 0x1440
TAB2 = 0x1640
ROW_END = 0x1E40
N = 128

if len(sys.argv) > 1:
    OUT = sys.argv[1]
if len(sys.argv) > 2:
    TRANS = sys.argv[2]
if len(sys.argv) > 3:
    ORIG = sys.argv[3]

items = json.load(open(ITEMS, encoding="utf-8"))
T = json.load(open(TRANS, encoding="utf-8"))
cf = load(ORIG)
row = [x for x in cf.rows if x["id"] == 2][0]
pt = bytearray(cf.plain(row))

base = struct.unpack_from("<I", pt, 0x18)[0]
size = struct.unpack_from("<I", pt, 0x1C)[0]
tab = struct.unpack_from("<I", pt, 0x20)[0]
cnt = struct.unpack_from("<I", pt, 0x24)[0]
assert (base, tab, cnt) == (BASE, TAB1, N), (base, tab, cnt)

orig_off = [struct.unpack_from("<I", pt, tab + i * 4)[0] for i in range(N)]
new_off = list(orig_off)
overflow = bytearray()

for x in items:
    i = x["i"]
    s = x["s"]
    es = T.get(s, "")
    if not es.strip():
        es = s
    b = es.encode("utf-8") + b"\x00"
    slot_start = orig_off[i]
    slot_end = orig_off[i + 1] if i + 1 < N else size
    if len(b) <= slot_end - slot_start:
        pt[base + slot_start:base + slot_end] = b + b"\x00" * (slot_end - slot_start - len(b))
    else:
        new_off[i] = ROW_END - BASE + len(overflow)
        overflow += b

for i in range(N):
    struct.pack_into("<I", pt, tab + i * 4, new_off[i])

newpt = bytes(pt) + bytes(overflow)
newrows = {2: (cf.cipher(row, newpt), len(newpt))}
blob = build_ordered(ORIG, newrows)
open(OUT, "wb").write(blob)
c2 = load(OUT)
for rr in c2.rows:
    assert rr["ex"] == len(c2.plain(rr)), (rr["id"], rr["ex"], len(c2.plain(rr)))
print("escrito", OUT, len(blob), "overflow", len(overflow), "verificado")
