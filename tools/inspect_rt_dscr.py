# -*- coding: utf-8 -*-
import struct
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

for p in [r"C:/Dev/Default Project/srwv/backup/MtZkn_Rt_original.cpk"]:
    cf = load(p)
    for f in cf.rows:
        d = bytes(b ^ 0x5E for b in cf.plain(f))
        i = d.find(b"DSCR")
        if i < 0:
            continue
        size = struct.unpack_from("<H", d, i + 4)[0]
        desc = d[i+6:i+6+size]
        if b"Mufti" in desc or b"regular" in desc:
            print("fila", f["id"], "size", size)
            print(repr(desc.decode("utf-8", "replace")))
