"""font_probe3.py - Guarda una tira vertical de la zona de 'e acute' (x=1220..1280,
y=300..420) ampliada, para ver exactamente donde esta el glifo y su altura."""
from cpk_util import load
from PIL import Image

cpk = 'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(cpk)
W = 4096
tex = cf.plain([r for r in cf.rows if r['id'] == 4][0])
img = Image.frombytes('L', (W, W), tex)
out = 'C:/Dev/Default Project/srwv/tools/_font_render'

c = img.crop((1180, 300, 1340, 420))
c = c.resize((160 * 4, 120 * 4), Image.NEAREST)
c.save(out + '/strip_eacute.png')
print('strip_eacute -> x1180..1340 y300..420')
