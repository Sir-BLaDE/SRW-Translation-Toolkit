"""font_vis.py - Renderiza glifos clave como imagenes PNG para inspeccion visual."""
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

def glyph_img(g, flip=False):
    u32, fl = rec(g)
    x = int(fl[0] * W); y = int(fl[1] * W)
    w = max(1, int(fl[2] * W)); h = max(1, int(fl[3] * W))
    rows = []
    for yy in range(h):
        yy2 = (W - y - h + yy) if flip else (y + yy)
        rows.append(tex[yy2 * W + x: yy2 * W + x + w])
    data = b''.join(rows)
    return u32, x, y, w, h, Image.frombytes('L', (w, h), data)

# recs de interes: id (u32) y lo que se espera
targets = [
    (0,   23450, 'rec0_id23450_esperado_0'),
    (11,  20999, 'rec11_id20999_esperado_a'),
    (15,  30331, 'rec15_id30331_esperado_e'),
    (215, 243,   'rec215_id243_esperado_o_acute'),
    (267, 201,   'rec267_id201_esperado_E_acute'),
    (268, 233,   'rec268_id233_esperado_e_acute'),
    (273, 232,   'rec273_id232_esperado_e_grave'),
    (274, 224,   'rec274_id224_esperado_a_grave'),
    (851, 12540, 'rec851_id12540_renders_bar'),
    (852, 12295, 'rec852_id12295_renders_O'),
]
for g, _, name in targets:
    u32, x, y, w, h, img = glyph_img(g)
    img.save('C:/Dev/Default Project/srwv/tools/_font_render/%s_g%03d.png' % (name, g))
    print('%s -> g%d id=%d pos(%d,%d) size %dx%d' % (name, g, u32, x, y, w, h))
