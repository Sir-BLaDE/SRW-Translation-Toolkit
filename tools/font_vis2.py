"""font_vis2.py - Renderiza rec 215 (id243=o acute) y 268 (id233=e acute) en
variantes sin flip y con flip vertical, para ver cual es correcta."""
from cpk_util import load
import struct
from PIL import Image

cpk = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(cpk)
W = 4096
p3 = cf.plain([r for r in cf.rows if r['id'] == 3][0])
tex = cf.plain([r for r in cf.rows if r['id'] == 4][0])
HDR = 40

def rec(g):
    off = HDR + g * 36
    u32 = struct.unpack_from('<I', p3, off)[0]
    fl = struct.unpack_from('<8f', p3, off + 4)
    return u32, fl

def save(g, flip, tag):
    u32, fl = rec(g)
    x = int(fl[0] * W); y = int(fl[1] * W)
    w = max(1, int(fl[2] * W)); h = max(1, int(fl[3] * W))
    rows = []
    for yy in range(h):
        yy2 = (W - y - h + yy) if flip else (y + yy)
        rows.append(tex[yy2 * W + x: yy2 * W + x + w])
    img = Image.frombytes('L', (w, h), b''.join(rows))
    # escalar x6 para verlo bien
    img = img.resize((w * 6, h * 6), Image.NEAREST)
    p = 'C:/Dev/Default Project/srwv/tools/_font_render/%s.png' % tag
    img.save(p)
    print(tag, 'g%d id=%d pos(%d,%d) %dx%d' % (g, u32, x, y, w, h))

for g in (215, 268, 267, 274):
    save(g, False, 'g%03d_noflip' % g)
    save(g, True, 'g%03d_flip' % g)
