# -*- coding: utf-8 -*-
import struct
import sys
sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

for p in [r"C:/Dev/Default Project/srwv/backup/MtZkn_Rt_original.cpk",
          r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/MtZkn_Rt.cpk"]:
    print("====", p)
    cf = load(p)
    for f in cf.rows:
        raw = cf.plain(f)
        for xor in (0, 0x5E):
            d = bytes(b ^ xor for b in raw)
            pos = 0
            while True:
                i = d.find(b"DSC2", pos)
                if i < 0:
                    break
                if i + 6 <= len(d):
                    size = struct.unpack_from("<H", d, i + 4)[0]
                    blob = d[i+6:i+6+size]
                    if b"regular" in blob or b"Mufti" in blob:
                        print("fila", f["id"], "xor", hex(xor), "off", i, "size", size)
                        print(repr(blob.decode("utf-8", "replace")))
                pos = i + 4
