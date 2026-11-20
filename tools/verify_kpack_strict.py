# -*- coding: utf-8 -*-\n"""Compara la estructura estricta de id4 entre el CPK anterior y el nuevo."""
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

OLD = r"C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_full_stable.cpk"
NEW = r"C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_full_stable2.cpk"


def align(v, a):
    return (v + a - 1) & ~(a - 1)


def strict(pt):
    cnt = struct.unpack_from("<I", pt, 0)[0]
    off = 0x10
    out = []
    while off + 0x40 <= len(pt):
        ln = struct.unpack_from("<I", pt, off + 0x3c)[0]
        if ln == 0 or ln > 0x400:
            break
        out.append((off, pt[off:off + 4], ln))
        off += 0x48 + align(ln, 4)
    return cnt, out, off


co, cn = load(OLD), load(NEW)
ao = co.plain([x for x in co.rows if x["id"] == 4][0])
bo = cn.plain([x for x in cn.rows if x["id"] == 4][0])
ca, ra, ea = strict(ao)
cb, rb, eb = strict(bo)
print("cabecera", ca, cb, "| registros", len(ra), len(rb),
      "| fin", hex(ea), hex(eb), "| total", hex(len(ao)))
print("misma secuencia de (offset,key,len):", ra == rb)
if ra != rb:
    for i, (x, y) in enumerate(zip(ra, rb)):
        if x != y:
            print("  dif en", i, x, y)
            break
# cabeceras de todas las filas identicas
for f in co.rows:
    a = co.plain(f)
    b = cn.plain([x for x in cn.rows if x["id"] == f["id"]][0])
    print("fila", f["id"], "longitud", len(a), len(b),
          "primeros 16 iguales", a[:16] == b[:16],
          "ultimos 16 iguales", a[-16:] == b[-16:])
