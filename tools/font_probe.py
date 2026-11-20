"""font_probe.py - Prueba definitiva: para los codepoints clave, localiza su
registro (id==codepoint) e imprime x,y,band. Ademas recorta el glifo usando y
tal cual y variantes (y, y-25, banda) para ver cual es correcto."""
from cpk_util import load
import struct
from PIL import Image

cpk = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(cpk)
W = 4096
p3 = cf.plain([r for r in cf.rows if r['id'] == 3][0])
tex = cf.plain([r for r in cf.rows if r['id'] == 4][0])
HDR = 40
img = Image.frombytes('L', (W, W), tex)
out = 'C:/Dev/Default Project/srwv/tools/_font_render'

def rec(g):
    off = HDR + g * 36
    u32 = struct.unpack_from('<I', p3, off)[0]
    fl = struct.unpack_from('<8f', p3, off + 4)
    return u32, fl

# indice codepoint -> registro
byc = {}
for g in range(1041):
    u32, fl = rec(g)
    byc.setdefault(u32, g)

for cp in [0x30, 0x61, 0xE9, 0xC9, 0xE0, 0xF3, 0xFC, 0xBF, 0xA1, 0xAB, 0xBB]:
    g = byc.get(cp)
    if g is None:
        print('U+%04X NO' % cp); continue
    u32, fl = rec(g)
    x = int(fl[0] * W); y = int(fl[1] * W)
    w = int(fl[2] * W); h = int(fl[3] * W)
    print('U+%04X %r -> g=%d x=%d y=%d w=%d h=%d  band=%d' % (cp, chr(cp), g, x, y, w, h, (y//40)*40))

# recortar glifos de acentos con varias hipotesis de y
def crop(cp, y0, tag):
    g = byc[cp]; u32, fl = rec(g)
    x = int(fl[0] * W); w = int(fl[2] * W); h = 44
    c = img.crop((x, y0, x + w, y0 + h))
    c = c.resize((w * 6, h * 6), Image.NEAREST)
    c.save('%s/%s.png' % (out, tag))
    print('crop', tag, 'x', x, 'y', y0)

for cp, name in [(0xE9, 'eacute'), (0xF3, 'oacute'), (0xC9, 'Eacute'), (0xE0, 'agrave')]:
    g = byc[cp]; u32, fl = rec(g)
    x = int(fl[0] * W); y = int(fl[1] * W)
    band = (y // 40) * 40
    crop(cp, y, name + '_asy')
    crop(cp, band, name + '_asband')
