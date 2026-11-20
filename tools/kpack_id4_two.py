# -*- coding: utf-8 -*-
"""Parchea dos titulos de escenario visibles en el id4 parcial de KPACK LN."""
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

SRC = r"C:/Dev/Default Project/srwv/backup/KPACK_P4_LN_EN_original.cpk"
BASE = r"C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_id4partial.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_id4partial2.cpk"

# textos que caben en 20 bytes con terminador nulo
PAIRS = {
    b"The Pirates of Mars": "Piratas de Marte",
    b"The Creeping Evil": "El mal acechante",
}

cf = load(SRC)
cb = load(BASE)
fb = [x for x in cb.rows if x["id"] == 4][0]
pt = bytearray(cb.plain(fb))
orig = [x for x in cf.rows if x["id"] == 4][0]
op = cf.plain(orig)
assert len(pt) == len(op)

changed = 0
for en, es in PAIRS.items():
    pos = op.find(en)
    assert pos >= 0, en
    assert pt[pos:pos + len(en)] == en, (en, "ya traducido?")
    field_len = 20  # longitud del campo segun el registro (u32 previo = 0x14)
    b = es.encode("utf-8") + b"\x00"
    assert len(b) <= field_len, (es, len(b))
    pt[pos:pos + field_len] = b + b"\x00" * (field_len - len(b))
    changed += 1

assert len(pt) == len(op)
blob = build_ordered(BASE, {4: (cb.cipher(fb, bytes(pt)), len(pt))})
open(OUT, "wb").write(blob)
c2 = load(OUT)
for r in c2.rows:
    assert r["ex"] == len(c2.plain(r)), (r["id"], r["ex"], len(c2.plain(r)))
print("cambiados", changed, "escrito", OUT, len(blob), "verificado")
