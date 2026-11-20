"""font_probe4.py - Recorta la fila real 8 (y=384..421) en la zona de acentos
(x=900..1600) ampliada, para ver los glifos acentuados de verdad."""
from cpk_util import load
from PIL import Image

cpk = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(cpk)
W = 4096
tex = cf.plain([r for r in cf.rows if r['id'] == 4][0])
img = Image.frombytes('L', (W, W), tex)
out = 'C:/Dev/Default Project/srwv/tools/_font_render'

for tag, x0, x1 in [('a', 940, 1300), ('b', 1300, 1660), ('c', 1660, 2020), ('d', 3400, 3700)]:
    c = img.crop((x0, 383, x1, 422))
    c = c.resize(((x1 - x0) * 5, 39 * 5), Image.NEAREST)
    c.save('%s/acc_%s.png' % (out, tag))
    print('acc_%s x%d..%d' % (tag, x0, x1))
