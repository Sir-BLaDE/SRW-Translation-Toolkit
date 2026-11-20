# -*- coding: utf-8 -*-\n"""Compara byte a byte las filas 2/4 viejas y nuevas para probar que solo\n cambiaron los huecos de texto, y recorre id4 usando el u32 declarado."""
import struct
import sys

sys.path.insert(0, r"C:/Dev/Default Project/srwv/tools")
from cpk_util import load

OLD = r"C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_full_stable.cpk"
NEW = r"C:/Dev/Default Project/srwv/outputs/KPACK_P4_LN_EN_full_stable2.cpk"


def align(v, a):
    return (v + a - 1) & ~(a - 1)


co, cn = load(OLD), load(NEW)


def ranges(a, b):
    out = []
    i = 0
    while i < len(a):
        if a[i] != b[i]:
            j = i
            while j < len(a) and a[j] != b[j]:
                j += 1
            out.append((i, j))
            i = j
        else:
            i += 1
    return out


for fid in (2, 4):
    a = co.plain([x for x in co.rows if x["id"] == fid][0])
    b = cn.plain([x for x in cn.rows if x["id"] == fid][0])
    rr = ranges(a, b)
    print("=== fila", fid, "longitud", len(a), len(b), "rangos cambiados", len(rr))
    # Los cambios deben caer dentro de un hueco de texto: antes del cambio
    # debe haber un u32 de longitud (id4) o ser un slot id2 conocido
    bad = 0
    for s, e in rr:
        if fid == 4:
            pre = struct.unpack_from("<I", a, s - 4)[0] if s >= 4 else 0
            slot_ok = e - s <= pre and pre <= 0x400
            if not slot_ok:
                bad += 1
                print("   RARO", hex(s), hex(e), "pre", pre)
        else:
            if (e - s) > 160:
                bad += 1
                print("   RARO", hex(s), hex(e))
    print("   rangos sospechosos", bad)
    print("   primeros:", [(hex(s), hex(e), e - s) for s, e in rr[:6]])

# Recorrido estricto de id4 usando SIEMPRE el u32 declarado en +0x3c
pt = cn.plain([x for x in cn.rows if x["id"] == 4][0])
cnt = struct.unpack_from("<I", pt, 0)[0]
off = 0x10
n = 0
while off + 0x40 <= len(pt):
    ln = struct.unpack_from("<I", pt, off + 0x3c)[0]
    if ln == 0 or ln > 0x400:
        break
    n += 1
    off += 0x48 + align(ln, 4)
print("=== id4 recorrido estricto: cabecera", cnt, "registros leidos", n,
      "fin", hex(off), "total", hex(len(pt)))
