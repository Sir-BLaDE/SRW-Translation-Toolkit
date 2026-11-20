"""font_measure.py - Mide la caja de tinta de cada glifo base en la textura EN (4096),
y localiza los huecos de acentos (puntos) y candidatos a sacrificar.

Salida pensada para decidir la geometria de composicion de acentos.
"""
from cpk_util import load
import struct

cpk = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(cpk)
rows = {r['id']: r for r in cf.rows}
p3 = cf.plain(rows[3])
tex = cf.plain(rows[4])
HDR = 40
W = 4096
N = (len(p3) - HDR) // 36


def rec(g):
    off = HDR + g * 36
    u32 = struct.unpack_from('<I', p3, off)[0]
    fl = struct.unpack_from('<8f', p3, off + 4)
    return u32, fl


def glyph(u32):
    off = HDR + u32 * 36
    gid = struct.unpack_from('<I', p3, off)[0]
    fl = struct.unpack_from('<8f', p3, off + 4)
    x = int(round(fl[0] * W)); y = int(round(fl[1] * W))
    w = int(round(fl[2] * W)); h = int(round(fl[3] * W))
    return gid, x, y, w, h, fl


byc = {}
for g in range(N):
    u, fl = rec(g)
    byc.setdefault(u, g)


def ink(rec_index):
    """Devuelve bbox de tinta relativo a la caja (x,y,w,h) o None."""
    gid, x, y, w, h, fl = glyph(rec_index)
    minx = miny = 10 ** 9
    maxx = maxy = -1
    for yy in range(h):
        base = (y + yy) * W + x
        row = tex[base:base + w]
        for xx, v in enumerate(row):
            if v:
                if xx < minx: minx = xx
                if xx > maxx: maxx = xx
                if yy < miny: miny = yy
                if yy > maxy: maxy = yy
    if maxx < 0:
        return gid, x, y, w, h, None, 0
    n = sum(1 for yy in range(miny, maxy + 1) for xx in range(minx, maxx + 1)
            if tex[(y + yy) * W + x + xx])
    return gid, x, y, w, h, (minx, miny, maxx, maxy), n


print('=== glifos base ===')
for cp in 'aeiounAEIOUN!?.,-':
    g = byc.get(ord(cp))
    if g is None:
        print(' %r NO' % cp); continue
    gid, x, y, w, h, bb, n = ink(g)
    print(' %r g=%4d box(%4d,%3d) %dx%d  ink=%s px=%d' % (cp, g, x, y, w, h, bb, n))

print()
print('=== huecos de acentos (registros con id latin-1) ===')
for cp in [0xE1, 0xC1, 0xE9, 0xC9, 0xED, 0xCD, 0xF3, 0xD3, 0xFA, 0xDA, 0xF1, 0xD1,
           0xFC, 0xDC, 0xBF, 0xA1, 0xAB, 0xBB, 0xE0, 0xC0, 0xE8, 0xEA, 0xEE, 0xF4, 0xFB,
           0xEB, 0xEF, 0xFF, 0xE7, 0xC7, 0xB4, 0xA8]:
    g = byc.get(cp)
    if g is None:
        print(' U+%04X %r NO EXISTE' % (cp, chr(cp))); continue
    gid, x, y, w, h, bb, n = ink(g)
    print(' U+%04X %r g=%4d box(%4d,%3d) ink=%s px=%d' % (cp, chr(cp), g, x, y, bb, n))

print()
print('=== candidatos a sacrificar: registros con <=8 px de tinta y cp>0x2FF ===')
cands = []
for g in range(N):
    u, fl = rec(g)
    if u < 0x2FF:
        continue
    gid, x, y, w, h, bb, n = ink(g)
    if n <= 8:
        cands.append((u, g, x, y, n))
print(' total candidatos:', len(cands))
for u, g, x, y, n in cands[:40]:
    print('   U+%04X %r g=%d pos(%d,%d) px=%d' % (u, chr(u), g, x, y, n))
