"""font_scan.py - Localiza las filas reales de glifos en la textura (perfil de tinta
por filas) y recorta las franjas para inspeccion."""
from cpk_util import load
from PIL import Image

cpk = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(cpk)
W = 4096
tex = cf.plain([r for r in cf.rows if r['id'] == 4][0])
img = Image.frombytes('L', (W, W), tex)
out = 'C:/Dev/Default Project/srwv/tools/_font_render'

# perfil de tinta por fila
nonzero = []
for y in range(0, 800):
    if max(tex[y * W: (y + 1) * W]) > 0:
        nonzero.append(y)
# agrupar en runs
runs = []
start = prev = nonzero[0]
for y in nonzero[1:]:
    if y == prev + 1:
        prev = y
    else:
        runs.append((start, prev))
        start = prev = y
runs.append((start, prev))
print('runs de filas con tinta:', runs)

for i, (a, b) in enumerate(runs):
    c = img.crop((0, a, W, b + 1))
    scale = 1
    c = c.resize((W, (b - a + 1) * 2), Image.NEAREST)
    c.save(out + '/row_%02d_y%d_%d.png' % (i, a, b))
    print('row_%02d y%d..%d' % (i, a, b))
