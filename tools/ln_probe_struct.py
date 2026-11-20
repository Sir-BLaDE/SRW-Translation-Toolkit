# -*- coding: utf-8 -*-\n"""Sonda la estructura real de id2 e id4 de KPACK LN."""
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load
import kpack_ln as k

P = r"C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_full_stable.cpk"
c = load(P)
pt2 = c.plain([x for x in c.rows if x["id"] == 2][0])
pt4 = c.plain([x for x in c.rows if x["id"] == 4][0])

print("=== id2 len", len(pt2))
print("head:", repr(pt2[:96]))
print("tail:", repr(pt2[-96:]))
# trailing zeros
z = 0
for b in reversed(pt2):
    if b == 0:
        z += 1
    else:
        break
print("trailing zero bytes:", z)

print()
print("=== id4 len", len(pt4))
cnt, recs = k.parse4(pt4)
print("header count", cnt, "parse4 recs", len(recs))
last = recs[-1]
print("last rec off", hex(last["off"]), "len", last["len"],
      "text", repr(last["text"][:60]))
end4 = last["off"] + 0x48 + k.align(last["len"] + 1, 4)
print("computed end after recs", hex(end4), "total", hex(len(pt4)))
print("bytes from end4:", repr(pt4[end4:end4 + 128]))
# search all NO ENCONTRADO strings
targets = [
    "-Return to Japan", "-The Original", "A Cause Worth Fighting For",
    "A Choice of Worlds", "A Letter to Tatsu", "Acting the Part",
    "Battle for the Three Earths", "Clash of the Mazin Redux",
    "Co-starring Beauty and Power", "Darker Than the Darkest Black",
    "Learning the Hathaway", "More Than Greed",
    "Power to Pierce Through Darkness", "Promise for a Fresh Start",
    "Stay or Go?", "The Dark Disciples", "The Gulf Between Past and Future",
    "The Reason We Live", "The Sins of Kaname Chidori",
    "Three Sisters of Axis", "Three Strengths", "Trouble in the LMC",
]
print()
print("=== localizacion de NO ENCONTRADO en id4 ===")
for t in targets:
    b = t.encode("utf-8")
    pos = pt4.find(b)
    if pos < 0:
        print("  NO ESTA", repr(t))
        continue
    # context: 32 before, 48 after
    print("  ", hex(pos), repr(t), "| ctx", repr(pt4[max(0, pos - 24):pos + len(b) + 24]))
