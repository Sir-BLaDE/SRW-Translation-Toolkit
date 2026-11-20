"""font_atlas.py - Guarda la textura de fuente entera y analiza el layout de glifos
sin numpy (Python puro, por bloques de 40px)."""
from cpk_util import load
from PIL import Image

cpk = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(cpk)
tex = cf.plain([r for r in cf.rows if r['id'] == 4][0])
W = 4096
img = Image.frombytes('L', (W, W), tex)
out = 'C:/Dev/Default Project/srwv/tools/_font_render'
img.resize((1024, 1024), Image.BILINEAR).save(out + '/atlas_full.png')
print('atlas ->', out + '/atlas_full.png')

# bandas de 40px con tinta
active = []
for band in range(0, W, 40):
    base = band * W
    chunk = tex[base:base + 40 * W]
    if max(chunk) > 0:
        active.append(band)
print('bandas de 40 con tinta (y):', active)

# celdas no vacias por banda, agrupadas
for band in active:
    base = band * W
    nz_cols = []
    for x in range(W):
        col_has = False
        for y in range(40):
            if tex[base + y * W + x]:
                col_has = True
                break
        if col_has:
            nz_cols.append(x)
    if nz_cols:
        print('banda y=%4d: x de %d a %d (%d columnas con tinta)' % (band, min(nz_cols), max(nz_cols), len(nz_cols)))
