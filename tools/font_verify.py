"""font_verify.py - Verifica el FontInfo parcheado leyendolo de nuevo."""
import struct
import sys

from cpk_util import load

p = sys.argv[1] if len(sys.argv) > 1 else 'C:/Dev/Default Project/srwv/outputs/FontInfo_es.cpk'
cf = load(p)
rows = {r['id']: r for r in cf.rows}
print('fichero:', p, '| entradas:', [(r['id'], r['size'], r['ex']) for r in cf.rows])
p1 = cf.plain(rows[1])
p3 = cf.plain(rows[3])
tex = cf.plain(rows[4])
W = 4096
HDR = 40
N = (len(p3) - HDR) // 36
print('metricas: %d registros | textura: %d bytes' % (N, len(tex)))

byc = {}
for g in range(N):
    u = struct.unpack_from('<I', p3, HDR + g * 36)[0]
    byc.setdefault(u, g)


def probe(cp):
    g = byc.get(cp)
    if g is None:
        print('  U+%04X %r  SIN REGISTRO' % (cp, chr(cp)))
        return
    off = HDR + g * 36
    fl = struct.unpack_from('<8f', p3, off + 4)
    x = int(round(fl[0] * W)); y = int(round(fl[1] * W))
    w = int(round(fl[2] * W)); h = int(round(fl[3] * W))
    npx = 0
    mnx = mny = 10 ** 9
    mxx = mxy = -1
    for yy in range(h):
        base = (y + yy) * W + x
        for xx in range(w):
            if tex[base + xx]:
                npx += 1
                mnx = min(mnx, xx); mxx = max(mxx, xx)
                mny = min(mny, yy); mxy = max(mxy, yy)
    bb = (mnx, mny, mxx, mxy) if mxx >= 0 else None
    pal = 'RELLENO' if bb == (0, 15, 5, 20) else 'ok'
    print('  %r U+%04X g=%4d box(%4d,%3d) bear=%.0f adv=%.0f ink_w=%.0f bb=%s px=%d %s'
          % (chr(cp), cp, g, x, y, fl[4], fl[5], fl[7], bb, npx, pal))


mapstr = p1[48:].decode('utf-8', 'ignore')
print('\n=== glifos nuevos ===')
for cp in [0xE1, 0xE9, 0xED, 0xF3, 0xFA, 0xF1, 0xC1, 0xC9, 0xD3, 0xDA, 0xFC, 0xA1, 0xBF]:
    probe(cp)
    if chr(cp) not in mapstr:
        print('     ^^ FALTA EN EL MAPA')

print('\n=== comprobacion de mapa ===')
for cp in [0xE1, 0xED, 0xFA, 0xF1, 0xC1, 0xD3, 0xDA, 0xE0, 0xE8, 0xF9, 0xE2, 0xEA, 0xEB, 0xEF]:
    print('  U+%04X %r en mapa: %s' % (cp, chr(cp), chr(cp) in mapstr))
print('  longitud del mapa:', len(p1))
print('  ASCII intacto:', all(chr(c) in mapstr for c in range(0x20, 0x7F)))
