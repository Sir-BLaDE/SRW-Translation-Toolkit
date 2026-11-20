# -*- coding: utf-8 -*-\n"""Compara donde viven los nombres de unidad: MTZKN, rpw_jstr y CMN00."""
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

G = r"D:/Juegos/-SPARROW-/Super Robot Wars V/"
names = [b"Emperor of Darkness", b"Evangelion Unit-00", b"Great Mazinger",
         b"Destiny Gundam", b"Guipellon-class Balgrey", b"Crossbone Gundam X-2 Kai",
         b"Emperador de la Oscuridad"]

srcs = {
    "MtZkn_Rt": G + "CommonData/MtData/EN/MtZkn_Rt.cpk",
    "rpw_jstr": G + "CommonData/MtData/EN/rpw_jstr.cpk",
    "CMN00": G + "Data/BTLC/EN0/CMN00.CPK",
    "KPACK_LN": G + "Data/KURODATA/EN/KPACK_P4_LN_EN.CPK",
}
cache = {}
for k, p in srcs.items():
    c = load(p)
    cache[k] = c
for n in names:
    print("===", n.decode())
    for k, c in cache.items():
        hits = 0
        dec_hits = 0
        for f in c.rows:
            pt = c.plain(f)
            if n in pt:
                hits += 1
            dec = bytes(b ^ 0x5E for b in pt)
            if n in dec:
                dec_hits += 1
        print("   %-9s raw=%d xor5E=%d" % (k, hits, dec_hits))
