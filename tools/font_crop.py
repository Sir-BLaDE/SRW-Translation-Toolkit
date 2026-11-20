"""font_crop.py - Recorta bandas de la textura para identificar glifos acentuados."""
from cpk_util import load
from PIL import Image

cpk = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(cpk)
tex = cf.plain([r for r in cf.rows if r['id'] == 4][0])
W = 4096
img = Image.frombytes('L', (W, W), tex)
out = 'C:/Dev/Default Project/srwv/tools/_font_render'

def crop_band(y0, y1, x0, x1, tag, scale=2):
    c = img.crop((x0, y0, x1, y1))
    c = c.resize(((x1 - x0) * scale, (y1 - y0) * scale), Image.NEAREST)
    c.save('%s/%s.png' % (out, tag))
    print(tag, 'y%d..%d x%d..%d' % (y0, y1, x0, x1))

# banda 360 (contiene rec 268 e acute y rec 215 o acute segun metricas)
crop_band(360, 410, 0, 1400, 'band360_left')
crop_band(360, 410, 1400, 2800, 'band360_mid')
crop_band(360, 410, 2800, 4096, 'band360_right')
