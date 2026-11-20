# -*- coding: utf-8 -*-
"""Describe cada chunk de lega_zkn y mide la relacion real de next/len."""
import re
import struct
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/lega_zkn.cpk"
cf = load(P)
pt = cf.plain(cf.rows[0])
print("len", len(pt))
print("header", [hex(struct.unpack_from("<I", pt, i)[0]) for i in (0x20, 0x24)])
for m in re.finditer(b"<chunk-head>\x00\x00\x00\x00", pt):
    i = m.start()
    name = pt[i+16:i+24].rstrip(b"\0").decode("ascii", "replace")
    nxt, length = struct.unpack_from("<II", pt, i+24)
    foot = pt.find(b"<chunk-foot>\x00\x00\x00\x00", i + 32)
    endc = pt.find(b"<endofchunk>\x00\x00\x00\x00", foot)
    payload = foot - (i + 32)
    fval = struct.unpack_from("<Q", pt, foot + 16)[0] if foot >= 0 else -1
    print("%-10s head=%06x next=%6d(%06x) len=%6d(%06x) payload=%6d foot=%06x end=%06x footval=%d next-len=%d next-(end+16-head)=%d" %
          (name, i, nxt, nxt, length, length, payload, foot, endc, fval,
           nxt - length, nxt - ((endc + 16) - i)))
