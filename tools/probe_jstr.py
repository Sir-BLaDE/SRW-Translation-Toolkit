# -*- coding: utf-8 -*-\n"""Analiza la estructura de rpw_jstr.cpk (chunk j-string)."""
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

P = r"D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/rpw_jstr.cpk"
c = load(P)
pt = c.plain(c.rows[0])
print("len", len(pt))
print("hex 0..192")
print(pt[:192].hex(" "))
print()
i = pt.find(b"j-string")
print("j-string at", hex(i))
print("bytes before:", repr(pt[max(0, i - 32):i]))
print("bytes after :", repr(pt[i:i + 48]))
# interpretar los 2 u32 tras 'j-string'
a, b = struct.unpack_from("<2I", pt, i + 8)
print("u32 tras j-string:", hex(a), hex(b), a, b)
# buscar una tabla de offsets creciente
for start in (i + 16, i + 8, a, b):
    if start + 8 <= len(pt):
        v = struct.unpack_from("<4I", pt, start)
        print("desde", hex(start), "->", [hex(x) for x in v])
# cuantos '\0rid_' hay
print("ocurrencias b'rid_':", pt.count(b"rid_"))
print("ocurrencias b'\\0rid_':", pt.count(b"\0rid_"))
# primer tramo tras cabecera
print("tras 8 bytes de j-string+16:", repr(pt[i + 16:i + 80]))
