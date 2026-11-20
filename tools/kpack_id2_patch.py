# -*- coding: utf-8 -*-
"""Parchea la descripcion de escenario visible en id2 de KPACK LN."""
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

SRC = r"C:/Dev/Default Project/srwv/backup/KPACK_P4_LN_EN_original.cpk"
BASE = r"C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_id4partial2.cpk"
OUT = r"C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_id4partial3.cpk"

EN = (b"Our hero, Lottie, and Velt team up as Robot Pilots.\n"
      b"Heading to Mars on the Yamato, they train together.")
ES = ("Nuestro héroe, Lottie y Velt se unen como pilotos.\n"
      "Rumbo a Marte en el Yamato, entrenan juntos.").encode("utf-8")

cf = load(SRC)
cb = load(BASE)
f = [x for x in cb.rows if x["id"] == 2][0]
pt = bytearray(cb.plain(f))
op = cf.plain([x for x in cf.rows if x["id"] == 2][0])
assert len(pt) == len(op)
pos = op.find(EN)
assert pos >= 0
assert pt[pos:pos + len(EN)] == EN
slot_end = op.find(b"\0", pos)
slot = slot_end - pos
print("EN len", len(EN), "slot", slot, "ES len", len(ES))
assert len(ES) <= slot - 1, ("no cabe", len(ES), slot)
pt[pos:pos + slot] = ES + b"\x00" * (slot - len(ES))

blob = build_ordered(BASE, {2: (cb.cipher(f, bytes(pt)), len(pt))})
open(OUT, "wb").write(blob)
c2 = load(OUT)
for r in c2.rows:
    assert r["ex"] == len(c2.plain(r)), (r["id"], r["ex"], len(c2.plain(r)))
print("escrito", OUT, len(blob), "verificado")
