# -*- coding: utf-8 -*-
import struct
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

for label, p in [("ORIG", r"C:/Dev/Default Project/srwv/backup/MtZkn_Rt_original.cpk"),
                 ("INST", r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/MtZkn_Rt.cpk")]:
    cf = load(p)
    for f in cf.rows:
        if f["id"] != 23:
            continue
        d = bytes(b ^ 0x5E for b in cf.plain(f))
        i = d.find(b"DSCR")
        size = struct.unpack_from("<H", d, i + 4)[0]
        tail = d[i + 6 + size:]
        print(label, "dscr size", size, "tail len", len(tail))
        print(repr(tail[:400]))
