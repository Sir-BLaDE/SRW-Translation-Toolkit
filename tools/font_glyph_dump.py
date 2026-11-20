import sys, struct
from PIL import Image, ImageDraw
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

p = sys.argv[1] if len(sys.argv)>1 else r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
out = sys.argv[2] if len(sys.argv)>2 else r'C:/Dev/Default Project/srwv/tools/_font_render/instalados.png'
cf = load(p); rows={r['id']:r for r in cf.rows}
p3=cf.plain(rows[3]); tex=cf.plain(rows[4]); W=4096; HDR=40; N=(len(p3)-HDR)//36
byc={}
for g in range(N):
    u=struct.unpack_from('<I',p3,HDR+g*36)[0]
    byc.setdefault(u,g)
def get(ch):
    g=byc[ord(ch)]; fl=struct.unpack_from('<8f',p3,HDR+g*36+4)
    x=int(round(fl[0]*W)); y=int(round(fl[1]*W)); w=int(round(fl[2]*W)); h=int(round(fl[3]*W))
    d=bytearray()
    for yy in range(h): d += tex[(y+yy)*W+x:(y+yy)*W+x+w]
    return Image.frombytes('L',(w,h),bytes(d))
chars=['a','á','e','é','i','í','o','ó','u','ú','n','ñ','A','Á','E','É','O','Ó','U','Ú','?','¿','!','¡']
tiles=[get(c).resize((80,88),Image.NEAREST) for c in chars]
sheet=Image.new('L',(6*90,4*98),30)
d=ImageDraw.Draw(sheet)
for i,(c,t) in enumerate(zip(chars,tiles)):
    x=(i%6)*90; y=(i//6)*98
    sheet.paste(t,(x,y)); d.text((x+2,y+88),c,fill=255)
sheet.save(out); print(out)
