"""font_check_glyphs.py - Comprueba si letras base y acentos existen DE VERDAD en la
textura, recortando por el registro cuyo id == codepoint. Guarda un contact sheet."""
from cpk_util import load
import struct
from PIL import Image

cpk = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(cpk)
W = 4096
p3 = cf.plain([r for r in cf.rows if r['id'] == 3][0])
tex = cf.plain([r for r in cf.rows if r['id'] == 4][0])
img = Image.frombytes('L', (W, W), tex)
HDR = 40
out = 'C:/Dev/Default Project/srwv/tools/_font_render'

def recg(g):
    off = HDR + g * 36
    u32 = struct.unpack_from('<I', p3, off)[0]
    fl = struct.unpack_from('<8f', p3, off + 4)
    return u32, fl

byc = {}
for g in range(1041):
    u32, fl = recg(g)
    byc.setdefault(u32, g)

def get(cp):
    g = byc.get(cp)
    if g is None:
        return None
    u32, fl = recg(g)
    x = int(fl[0] * W); y = int(fl[1] * W); w = int(fl[2] * W); h = int(fl[3] * W)
    return g, x, y, w, h

cps = [(0x65, 'e'), (0x6E, 'n'), (0x61, 'a'), (0x69, 'i'), (0x6F, 'o'),
       (0x75, 'u'), (0x41, 'A'), (0x4F, 'O'), (0x55, 'U'),
       (0xB4, 'acute'), (0x7E, 'tilde'), (0xA8, 'diaer'), (0x5E, 'circ'),
       (0xE9, 'eacute'), (0xC9, 'Eacute'), (0xF3, 'oacute'), (0xE0, 'agrave')]

tiles = []
for cp, name in cps:
    r = get(cp)
    if r is None:
        print('%-8s U+%04X NO' % (name, cp)); continue
    g, x, y, w, h = r
    crop = img.crop((x, y, x + max(w, 1), y + max(h, 1)))
    print('%-8s U+%04X g=%d pos(%d,%d) %dx%d' % (name, cp, g, x, y, w, h))
    tiles.append((name, crop))

# contact sheet 6 columnas, cada tile escalada x4 y con etiqueta separada por lineas
scale = 4
cw = 48 * scale
ch = 48 * scale
cols = 6
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new('L', (cols * cw, rows * ch), 32)
for i, (name, crop) in enumerate(tiles):
    crop = crop.resize((crop.width * scale, crop.height * scale), Image.NEAREST)
    r_, c_ = divmod(i, cols)
    sheet.paste(crop, (c_ * cw, r_ * ch))
sheet.save(out + '/contact_base.png')
print('contact -> contact_base.png', [n for n, _ in tiles])
