"""font_probe2.py - Verifica la textura: recorta '0' (g1035 x220 y1) y 'a' (g1024 x704 y1)
y ademas perfila verticalmente la columna x=1232 para localizar el glifo 'e acute'."""
from cpk_util import load
import struct
from PIL import Image

cpk = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(cpk)
W = 4096
tex = cf.plain([r for r in cf.rows if r['id'] == 4][0])
img = Image.frombytes('L', (W, W), tex)
out = 'C:/Dev/Default Project/srwv/tools/_font_render'

def crop(x, y, w, h, tag, scale=6):
    c = img.crop((x, y, x + w, y + h))
    c = c.resize((w * scale, h * scale), Image.NEAREST)
    c.save('%s/%s.png' % (out, tag))
    print(tag)

crop(220, 1, 40, 44, 'chk_zero')
crop(704, 1, 40, 44, 'chk_a')

# perfil vertical en x=1232..1272
print('perfil vertical x=1232..1272 (y con tinta):')
runs = []
for y in range(0, 700):
    row = tex[y * W + 1232: y * W + 1272]
    if max(row) > 0:
        runs.append(y)
print('ys con tinta:', runs[:5], '...', runs[-5:] if runs else 'NINGUNO', 'total', len(runs))

# perfiles de otras columnas de la zona de acentos para comprobar
for x in (968, 1232, 1276, 1848, 3564):
    ys = [y for y in range(0, 700) if max(tex[y * W + x: y * W + x + 40]) > 0]
    if ys:
        print('x=%d: y de %d a %d (%d filas)' % (x, min(ys), max(ys), len(ys)))
    else:
        print('x=%d: SIN TINTA' % x)
