"""font_jp2.py - Localiza en la textura JP (8192x8192) los glifos acentuados y
guarda recortes para comparar con EN."""
from cpk_util import load
import struct, os
from PIL import Image

cpk = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/JP/FontInfo.cpk'
cf = load(cpk)
rows = {r['id']: r for r in cf.rows}
p3 = cf.plain(rows[3])
tex = cf.plain(rows[4])
HDR = 40
N = (len(p3) - HDR) // 36
W = 8192
print('registros JP:', N, 'textura', len(tex), '=> W =', int(len(tex) ** 0.5))

img = Image.frombytes('L', (W, W), tex)
out = 'C:/Dev/Default Project/srwv/tools/_font_render'

def rec(g):
    off = HDR + g * 36
    u32 = struct.unpack_from('<I', p3, off)[0]
    fl = struct.unpack_from('<8f', p3, off + 4)
    return u32, fl

byc = {}
for g in range(N):
    u32, fl = rec(g)
    byc.setdefault(u32, g)

cps = [(0x65, 'e'), (0x61, 'a'), (0x6F, 'o'), (0x6E, 'n'), (0x75, 'u'), (0x69, 'i'),
       (0x41, 'A'), (0x45, 'E'), (0x4F, 'O'), (0x55, 'U'), (0x4E, 'N'),
       (0xE9, 'eacute'), (0xC9, 'Eacute'), (0xE1, 'aacute'), (0xED, 'iacute'),
       (0xF3, 'oacute'), (0xFA, 'uacute'), (0xF1, 'ntilde'), (0xC1, 'Aacute'),
       (0xD3, 'Oacute'), (0xDA, 'Uacute'), (0xC3, 'Atilde'), (0xD1, 'Ntilde'),
       (0xFC, 'udiaer'), (0xBF, 'invq'), (0xA1, 'inve'), (0xAB, 'laquo'), (0xBB, 'raquo'),
       (0xB4, 'acute')]

found = {}
for cp, name in cps:
    g = byc.get(cp)
    if g is None:
        print('%-8s U+%04X NO EXISTE' % (name, cp))
        continue
    u32, fl = rec(g)
    x = int(fl[0] * W); y = int(fl[1] * W); w = int(fl[2] * W); h = int(fl[3] * W)
    found[name] = (g, x, y, w, h)
    print('%-8s U+%04X g=%5d pos(%5d,%5d) %dx%d' % (name, cp, g, x, y, w, h))

os.makedirs(out, exist_ok=True)
tiles = []
for name, (g, x, y, w, h) in found.items():
    if w <= 0 or h <= 0:
        continue
    c = img.crop((x, y, x + w, y + h))
    c = c.resize((w * 3, h * 3), Image.NEAREST)
    c.save('%s/jp_%s.png' % (out, name))
    tiles.append((name, c))

if tiles:
    cols = 6
    cw = max(t[1].width for t in tiles) + 8
    ch = max(t[1].height for t in tiles) + 8
    rws = (len(tiles) + cols - 1) // cols
    sheet = Image.new('L', (cols * cw, rws * ch), 32)
    for i, (name, c) in enumerate(tiles):
        r_, c_ = divmod(i, cols)
        sheet.paste(c, (c_ * cw, r_ * ch))
    sheet.save(out + '/jp_contact.png')
    print('contact ->', out + '/jp_contact.png', [t[0] for t in tiles])
