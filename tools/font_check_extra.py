"""font_check_extra.py - Comprueba si ciertos signos tipograficos existen en el mapa
(id1) y tienen glifo real (no cuadrado de relleno) en la textura."""
from cpk_util import load
import struct

cpk = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(cpk)
rows = {r['id']: r for r in cf.rows}
p1 = cf.plain(rows[1])
p3 = cf.plain(rows[3])
tex = cf.plain(rows[4])
HDR = 40
W = 4096
N = (len(p3) - HDR) // 36

# decodificar strings del mapa: zona 48.. hasta el ultimo byte no nulo
strings = p1[48:]
groups = strings.split(b'\x00')
mapchars = set()
for gb in groups:
    try:
        s = gb.decode('utf-8')
    except UnicodeDecodeError:
        continue
    for ch in s:
        mapchars.add(ch)
print('chars en mapa:', len(mapchars))

byc = {}
for g in range(N):
    off = HDR + g * 36
    u = struct.unpack_from('<I', p3, off)[0]
    byc.setdefault(u, g)


def glyph(u):
    off = HDR + u * 36
    gid = struct.unpack_from('<I', p3, off)[0]
    fl = struct.unpack_from('<8f', p3, off + 4)
    x = int(round(fl[0] * W)); y = int(round(fl[1] * W))
    w = int(round(fl[2] * W)); h = int(round(fl[3] * W))
    gid2, x2, y2, w2, h2 = gid, x, y, w, h
    bb = None
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
    if mxx >= 0:
        bb = (mnx, mny, mxx, mxy)
    return x, y, w, h, bb, npx


def report(ch):
    g = byc.get(ord(ch))
    inmap = ch in mapchars
    if g is None:
        print(' %r U+%04X  mapa=%s  glifo=NO EXISTE' % (ch, ord(ch), inmap))
        return
    x, y, w, h, bb, npx = glyph(g)
    kind = 'REAL'
    if bb == (0, 15, 5, 20) and npx == 36:
        kind = 'RELLENO(cuadrado)'
    elif npx == 0:
        kind = 'VACIO'
    print(' %r U+%04X  mapa=%-5s  g=%4d box(%4d,%3d) %dx%d ink=%s px=%d  %s'
          % (ch, ord(ch), inmap, g, x, y, w, h, bb, npx, kind))


for ch in '«»—–―…‘’“”ºª～·¡¿°%€$':
    report(ch)
