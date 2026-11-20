# -*- coding: utf-8 -*-
"""SysText fila 2 traducida, almacenada SIN compresion CRILAYLA."""
import json
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

ORIG = r"C:/Dev/Default Project/srwv/backup/SysText_antes_es.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/SysText_es_raw.cpk"
ITEMS = r"C:/Dev/Default Project/srwv/datos/systext_row2.json"
TRANS = r"C:/Dev/Default Project/srwv/datos/systext_trans.json"
BASE, TAB1, ROW_END, N = 0x30, 0x1440, 0x1E40, 128

if len(sys.argv) > 1:
    OUT = sys.argv[1]
if len(sys.argv) > 2:
    TRANS = sys.argv[2]

items = json.load(open(ITEMS, encoding="utf-8"))
T = json.load(open(TRANS, encoding="utf-8"))
cf = load(ORIG)
row = [x for x in cf.rows if x["id"] == 2][0]
pt = bytearray(cf.plain(row))

base = struct.unpack_from("<I", pt, 0x18)[0]
tab = struct.unpack_from("<I", pt, 0x20)[0]
assert (base, tab) == (BASE, TAB1)
orig_off = [struct.unpack_from("<I", pt, tab + i * 4)[0] for i in range(N)]
new_off = list(orig_off)
overflow = bytearray()

for x in items:
    i, s = x["i"], x["s"]
    es = T.get(s, "") or s
    b = es.encode("utf-8") + b"\x00"
    start, end = orig_off[i], (orig_off[i + 1] if i + 1 < N else struct.unpack_from("<I", pt, 0x1C)[0])
    if len(b) <= end - start:
        pt[base + start:base + end] = b + b"\x00" * (end - start - len(b))
    else:
        new_off[i] = ROW_END - BASE + len(overflow)
        overflow += b

for i in range(N):
    struct.pack_into("<I", pt, tab + i * 4, new_off[i])

newpt = bytes(pt) + bytes(overflow)
blob = build_ordered(ORIG, {2: (newpt, len(newpt))})
open(OUT, "wb").write(blob)
cf2 = load(OUT)
for r in cf2.rows:
    assert r["ex"] == len(cf2.plain(r)), (r["id"], r["ex"], len(cf2.plain(r)))
print("escrito", OUT, len(blob), "overflow", len(overflow), "verificado")
