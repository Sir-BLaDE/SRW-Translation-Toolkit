"""font_bands.py - Para cada banda de 40px de la textura, lista los registros de
metrica cuyo y cae en esa banda, con su id como caracter Unicode. Permite ver el
layout real y localizar los glifos acentuados."""
from cpk_util import load
import struct, unicodedata

cpk = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(cpk)
W = 4096
p3 = cf.plain([r for r in cf.rows if r['id'] == 3][0])
HDR = 40

def rec(g):
    off = HDR + g * 36
    u32 = struct.unpack_from('<I', p3, off)[0]
    fl = struct.unpack_from('<8f', p3, off + 4)
    return u32, fl

def ch(u32):
    try:
        c = chr(u32)
        if unicodedata.category(c) in ('Cc', 'Cn', 'Cs'):
            return '?'
        return c
    except Exception:
        return '?'

bands = {}
for g in range(1041):
    u32, fl = rec(g)
    y = int(fl[1] * W)
    x = int(fl[0] * W)
    w = int(fl[2] * W)
    band = (y // 40) * 40
    bands.setdefault(band, []).append((x, g, u32, w))

for band in sorted(bands):
    items = sorted(bands[band])
    s = ''.join(ch(u) for _, _, u, _ in items)
    print('=== banda y=%4d  (%d glifos) ===' % (band, len(items)))
    print('  chars:', s[:80])
    # imprimir x de los que son latinos acentuados
    acc = [(x, g, u, w) for x, g, u, w in items if 0xA0 <= u <= 0xFF]
    if acc:
        print('  acentos latin1 en esta banda:')
        for x, g, u, w in acc:
            print('    x=%4d g=%3d U+%04X %r w=%d' % (x, g, u, ch(u), w))
