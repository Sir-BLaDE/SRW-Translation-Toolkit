# -*- coding: utf-8 -*-
"""Muestra las cadenas de la fila 2 de SysText por indice."""
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = sys.argv[1] if len(sys.argv) > 1 else r"D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/SysText.cpk"
c = load(P)
r = [x for x in c.rows if x["id"] == 2][0]
pt = c.plain(r)
base = struct.unpack_from("<I", pt, 0x18)[0]
size = struct.unpack_from("<I", pt, 0x1C)[0]
tab = struct.unpack_from("<I", pt, 0x20)[0]
cnt = struct.unpack_from("<I", pt, 0x24)[0]
print("base", hex(base), "size", hex(size), "tab", hex(tab), "cnt", cnt, "len", len(pt))
offs = [struct.unpack_from("<I", pt, tab + i * 4)[0] for i in range(cnt)]
for i in range(cnt):
    st = base + offs[i]
    en = pt.find(b"\x00", st)
    s = pt[st:en].decode("utf-8", "replace")
    if i < 60 or "Terrain" in s or "Emperor" in s or "Darkness" in s or "Aestivalis" in s or "Beam" in s or "Kurogane" in s:
        print("%3d %r" % (i, s[:80]))
