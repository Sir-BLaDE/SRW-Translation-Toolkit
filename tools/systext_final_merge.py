# -*- coding: utf-8 -*-
"""Reconstruye SysText: fila 2 desde el original con el mapa corregido y
conserva la fila 0 ya traducida del output actual."""
import io
import json
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

ORIG = r"C:/Dev/Default Project/srwv/backup/SysText_antes_es.cpk"
CUR = r"C:/Dev/Default Project/srwv/outputs/SysText_es.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/SysText_es_final.cpk"
ITEMS = r"C:/Dev/Default Project/srwv/datos/systext_row2.json"
TRANS = r"C:/Dev/Default Project/srwv/datos/systext_trans.json"
BASE, TAB1, TAB2, ROW_END, N = 0x30, 0x1440, 0x1640, 0x1E40, 128

items = json.load(io.open(ITEMS, encoding="utf-8"))
T = json.load(io.open(TRANS, encoding="utf-8"))
orig = load(ORIG)
cur = load(CUR)
row2o = [x for x in orig.rows if x["id"] == 2][0]
row0c = [x for x in cur.rows if x["id"] == 0][0]

pt = bytearray(orig.plain(row2o))
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
    es = T.get(x["s"], x["s"])
    if not es.strip():
        es = x["s"]
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
newpt2 = bytes(pt) + bytes(overflow)

newrows = {
    0: (cur.cipher(row0c, cur.plain(row0c)), len(cur.plain(row0c))),
    2: (orig.cipher(row2o, newpt2), len(newpt2)),
}
blob = build_ordered(ORIG, newrows)
with io.open(OUT, "wb") as f:
    f.write(blob)
chk = load(OUT)
for r in chk.rows:
    assert r["ex"] == len(chk.plain(r)), (r["id"], r["ex"], len(chk.plain(r)))
row2 = [r for r in chk.rows if r["id"] == 2][0]
pt2 = chk.plain(row2)
base2 = struct.unpack_from("<I", pt2, 0x18)[0]
tab2 = struct.unpack_from("<I", pt2, 0x20)[0]
cnt2 = struct.unpack_from("<I", pt2, 0x24)[0]
vals = []
for i in range(cnt2):
    v = struct.unpack_from("<I", pt2, tab2 + i * 4)[0]
    vals.append(pt2[base2 + v:].split(b"\x00")[0].decode("utf-8", "ignore"))
print("escrito", OUT, len(blob), "overflow", len(overflow))
print("SysText[16] =", repr(vals[16]))
print("Newtype artificial en banco:", sum("Newtype artificial" in s for s in vals))
