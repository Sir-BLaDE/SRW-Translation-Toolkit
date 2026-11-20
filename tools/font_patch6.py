"""font_patch6.py - copia los glifos con acento agudo de Yu Gothic Medium
(la fuente del sistema mas parecida a la del juego, IoU 0.918), alineando la
letra base con la del juego. El resto (ñ, ¿, ¡, ü) se deja como en es5.
"""
import os, struct, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
import font_patch as fp
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

BASE = r'C:/Dev/Default Project/srwv/outputs/FontInfo_es5.cpk'
ORIG = r'C:/Dev/Default Project/srwv/backup/FontInfo_EN_original.cpk'
OUT  = r'C:/Dev/Default Project/srwv/outputs/FontInfo_es6.cpk'
SRC_FONT = r'C:/Windows/Fonts/YuGothM.ttc'
SRC_IDX  = 0
SRC_SIZE = 38
W, HDR = 4096, 40

ACUTE = [
    ('á','a'), ('é','e'), ('í','i'), ('ó','o'), ('ú','u'),
    ('Á','A'), ('É','E'), ('Í','I'), ('Ó','O'), ('Ú','U'),
]

font = fp.Font(BASE)
srcfont = ImageFont.truetype(SRC_FONT, SRC_SIZE, index=SRC_IDX)
CANVAS = SRC_SIZE * 4
ORIGIN = SRC_SIZE

def render_src(ch):
    im = Image.new('L', (CANVAS, CANVAS), 0)
    ImageDraw.Draw(im).text((ORIGIN, ORIGIN), ch, font=srcfont, fill=255)
    return im

def ink_bbox(img):
    return img.point(lambda v: 255 if v > 90 else 0).getbbox()

for ch, base in ACUTE:
    g = font.rec_of(ch)
    gb = font.rec_of(base)
    # caja del glifo en el juego
    cw, chh = font.box(g)[2:]
    game_base = font.get(gb)
    gbb = ink_bbox(game_base)
    # render de la fuente fuente: base y acentuado con el mismo origen
    sbase = render_src(base); sacc = render_src(ch)
    sbb = ink_bbox(sbase); abb = ink_bbox(sacc)
    # desplazamiento para alinear la base de la fuente con la base del juego
    dx = gbb[0] - sbb[0]
    dy = gbb[1] - sbb[1]
    # recortar el glifo acentuado y pegarlo en una caja vacia del juego
    crop = sacc.crop(abb)
    dest = Image.new('L', (cw, chh), 0)
    px = abb[0] + dx; py = abb[1] + dy
    dest.paste(crop, (px, py))
    # metricas: copiar bearing/avance de la base del juego
    _, base_fl = font.rec(gb)
    _, fl = font.rec(g)
    fl[4] = base_fl[4]; fl[5] = base_fl[5]
    # ancho de tinta = extremo derecho real
    fl[7] = float(max(0, px + crop.width))
    font.put(g, dest); font.write_rec(g, ord(ch), fl)
    print(' %r<- %r  src=%s base_src=%s game_base=%s dx=%d dy=%d -> caja=%s ink=%d' %
          (ch, base, abb, sbb, gbb, dx, dy, dest.size, fl[7]))

# Guardar (los mapas ya estan en es5)
new = {}
for fid in (1, 2, 3, 4):
    f = font.rows[fid]; plain = bytes(font.p1 if fid == 1 else
                                      (font.p3 if fid == 3 else font.tex))
    if fid == 2:
        plain = bytes(font.cf.plain(f))
    new[fid] = (font.cf.cipher(f, plain), len(plain))
blob = build_ordered(ORIG, new)
open(OUT, 'wb').write(blob)
c2 = load(OUT)
for rr in c2.rows: assert rr['ex'] == len(c2.plain(rr)), rr
print('escrito', OUT, len(blob), 'verificado')
