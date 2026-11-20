"""font_patch7.py - toma SOLO la marca del acento agudo de Yu Gothic Medium
(la fuente mas parecida al juego) y la pega sobre la letra original del juego,
de modo que el dibujo de la letra no cambia. Corrige sobre todo la 'í', cuyo
acento estaba flotando 7 filas por encima del asta.
El resto (ñ, ¿, ¡, ü) se deja como en es5.
"""
import sys, struct
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
import font_patch as fp
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

BASE = r'C:/Dev/Default Project/srwv/outputs/FontInfo_es5.cpk'
ORIG = r'C:/Dev/Default Project/srwv/backup/FontInfo_EN_original.cpk'
OUT  = r'C:/Dev/Default Project/srwv/outputs/FontInfo_es7.cpk'
SRC_FONT = r'C:/Windows/Fonts/YuGothM.ttc'
SRC_SIZE = 38
W, HDR = 4096, 40

ACUTE = [
    ('á','a'), ('é','e'), ('í','i'), ('ó','o'), ('ú','u'),
    ('Á','A'), ('É','E'), ('Í','I'), ('Ó','O'), ('Ú','U'),
]

font = fp.Font(BASE)
src = ImageFont.truetype(SRC_FONT, SRC_SIZE, index=0)
CANVAS = SRC_SIZE * 4
ORIGIN = SRC_SIZE

def bbox(img, thr=90):
    return img.point(lambda v: 255 if v > thr else 0).getbbox()

def render(ch):
    im = Image.new('L', (CANVAS, CANVAS), 0)
    ImageDraw.Draw(im).text((ORIGIN, ORIGIN), ch, font=src, fill=255)
    return im

def accent_mark(ch, base):
    """Recorta solo la marca de acento. El acento es el componente superior:
    se buscan las filas con tinta desde arriba hasta el primer hueco en blanco."""
    acc = render(ch)
    abb = bbox(acc)
    if not abb:
        return Image.new('L',(1,1),0)
    x0, y0, x1, y1 = abb
    # primera fila completamente en blanco por debajo del inicio de tinta
    gap = None
    for yy in range(y0, min(y1, y0+16)):
        row = [acc.getpixel((xx,yy)) for xx in range(x0,x1)]
        if all(v <= 30 for v in row):
            gap = yy
            break
    if gap is None:
        gap = y0 + 6
    region = acc.crop((x0, y0, x1, gap))
    mb = bbox(region)
    return region.crop(mb) if mb else region

for ch, base in ACUTE:
    g = font.rec_of(ch)
    gb = font.rec_of(base)
    cw, chh = font.box(g)[2:]
    game_base = font.get(gb)          # letra original del juego (sin acento)
    gbb = bbox(game_base)
    mark = accent_mark(ch, base)
    upper = base.isupper()
    # mayusculas: poco espacio arriba -> reducir la marca a 3 filas
    if upper and mark.height > 3:
        f = 3.0 / mark.height
        mark = mark.resize((max(1,int(round(mark.width*f))), 3), Image.LANCZOS)
    img = game_base.copy()
    px = img.load()
    if base == 'i':
        # quitar el punto (filas 4..7) y colocar el acento ahi
        for yy in range(gbb[1], gbb[1]+4):
            for xx in range(gbb[0], gbb[2]):
                px[xx, yy] = 0
        bottom = gbb[1] + 4
    else:
        bottom = gbb[1] - 2
    top = bottom - mark.height + 1
    ax = max(0, gbb[0] + (gbb[2]-gbb[0] - mark.width)//2)
    img.paste(mark, (ax, top))
    _, base_fl = font.rec(gb)
    _, fl = font.rec(g)
    fl[4] = base_fl[4]; fl[5] = base_fl[5]
    fl[7] = float(max(gbb[2], ax + mark.width))
    font.put(g, img); font.write_rec(g, ord(ch), fl)
    print(' %r base=%r mark=%s top=%d bottom=%d ax=%d' % (ch,base,mark.size,top,bottom,ax))

new = {}
for fid in (1, 2, 3, 4):
    f = font.rows[fid]
    plain = bytes(font.p1 if fid == 1 else (font.p3 if fid == 3 else font.tex))
    if fid == 2:
        plain = bytes(font.cf.plain(f))
    new[fid] = (font.cf.cipher(f, plain), len(plain))
blob = build_ordered(ORIG, new)
open(OUT, 'wb').write(blob)
c2 = load(OUT)
for rr in c2.rows: assert rr['ex'] == len(c2.plain(rr)), rr
print('escrito', OUT, len(blob), 'verificado')
