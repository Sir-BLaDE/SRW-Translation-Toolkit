"""font_patch4.py - como font_patch3, pero el acento agudo se toma del glifo
` (U+0060) girado 180 grados: es una diagonal fina del mismo estilo que la
fuente, en vez de la barra gruesa de U+00B4 que se veia rara.
"""
import os, struct, sys
from PIL import Image, ImageDraw
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
import font_patch as fp
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

ORIG = r'C:/Dev/Default Project/srwv/backup/FontInfo_EN_original.cpk'
OUT  = r'C:/Dev/Default Project/srwv/outputs/FontInfo_es4.cpk'
W, HDR = 4096, 40

REUSE = [0xE0, 0xE8, 0xF9, 0xE2, 0xEA, 0xEB, 0xEF, 0x178]
ADD   = [0xE1, 0xED, 0xFA, 0xF1, 0xC1, 0xD3, 0xDA, 0xCD]

# (destino, base, acento)  acento: 'acute' | 'tilde' | 'dia' | 'invertido'
GLYPHS = [
 ('á','a','acute'), ('é','e','acute'), ('í','i','acute'),
 ('ó','o','acute'), ('ú','u','acute'), ('ñ','n','tilde'),
 ('Á','A','acute'), ('É','E','acute'), ('Í','I','acute'),
 ('Ó','O','acute'), ('Ú','U','acute'), ('ü','u','dia'),
 ('¿','?','invertido'), ('¡','!','invertido'),
]

font = fp.Font(ORIG)

def ink_bbox(img):
    px=img.load(); mnx=mny=10**9; mxx=mxy=-1
    for yy in range(img.height):
        for xx in range(img.width):
            if px[xx,yy]>30:
                mnx=min(mnx,xx); mxx=max(mxx,xx); mny=min(mny,yy); mxy=max(mxy,yy)
    return None if mxx<0 else (mnx,mny,mxx,mxy)

def accent_img(ch, rotate=False):
    g=font.rec_of(ch)
    img=font.get(g).copy()
    bb=ink_bbox(img)
    img=img.crop((bb[0],bb[1],bb[2]+1,bb[3]+1))
    if rotate:
        img=img.transpose(Image.ROTATE_180)
    return img

# acento agudo: grave (`) girado 180°. tilde y dieresis sin girar.
ACC_IMGS = {
 'acute': accent_img('`',rotate=True),
 'tilde': accent_img('~'),
 'dia':   accent_img('¨'),
}
print('acentos:',{k:v.size for k,v in ACC_IMGS.items()})

targets={}
reuse_it=iter(REUSE)
for ch,base,kind in GLYPHS:
    g=font.byc.get(ord(ch))
    if g is None:
        cp=next(reuse_it); g=font.byc[cp]
    targets[ch]=(g,ord(ch))

for ch,base,kind in GLYPHS:
    g,_=targets[ch]
    gb=font.rec_of(base)
    base_img=font.get(gb).copy()
    _, base_fl=font.rec(gb)
    base_bb=ink_bbox(base_img)
    img=base_img
    if kind=='invertido':
        x0,y0,x1,y1=base_bb
        crop=base_img.crop((x0,y0,x1+1,y1+1)).transpose(Image.ROTATE_180)
        blank=Image.new('L',img.size,0); blank.paste(crop,(x0,y0)); img=blank
    else:
        acc=ACC_IMGS[kind].copy()
        if base=='i':
            d=ImageDraw.Draw(img); d.rectangle([0,4,img.width-1,9],fill=0)
            top_y=4
        else:
            top_y=base_bb[1]
        cx=(base_bb[0]+base_bb[2])/2.0
        ax=int(round(cx-(acc.width-1)/2.0))
        ay=int(max(0, top_y-3-acc.height))
        img.paste(acc,(ax,ay))
    _, fl=font.rec(g)
    fl[4]=base_fl[4]; fl[5]=base_fl[5]
    newbb=ink_bbox(img)
    fl[7]=float(newbb[2]+1)
    font.put(g,img); font.write_rec(g,ord(ch),fl)
    print(' %r g=%-4d base=%r b=%.0f a=%.0f bb=%s'%(ch,g,base,fl[4],fl[5],newbb))

# mapa fila 1
p1=bytes(font.p1)
for old,new in zip(REUSE+[0xFF],ADD+[0xF3]):
    ob=chr(old).encode('utf-8'); nb=chr(new).encode('utf-8')
    assert len(ob)==len(nb)==2 and p1.count(ob)==1,(hex(old),p1.count(ob))
    i=p1.index(ob); p1=p1[:i]+nb+p1[i+2:]
font.p1=bytearray(p1)

# mapa fila 2
R2_OLD=list('ЁЪЫЬЭЮЯёъыьэюя')
R2_NEW=list('áéíóúñÁÉÍÓÚü¿¡')
r=font.rows[2]; p2=bytearray(font.cf.plain(r))
h=[struct.unpack_from('<I',p2,i*4)[0] for i in range(12)]
a,b=h[6],h[7]
s=bytes(p2[a:b])
for old,new in zip(R2_OLD,R2_NEW):
    ob=old.encode('utf-8'); nb=new.encode('utf-8')
    assert len(ob)==len(nb)==2 and s.count(ob)==1,(old,s.count(ob))
    i=s.index(ob); p2[a+i:a+i+2]=nb

CHARS=list('áéíóúñÁÉÍÓÚü¿¡')
for rid,data in [(1,bytes(font.p1)),(2,bytes(p2))]:
    hh=[struct.unpack_from('<I',data,i*4)[0] for i in range(12)]
    ss=data[hh[6]:hh[7]].decode('utf-8','ignore')
    missing=[c for c in CHARS if c not in ss]
    assert not missing,'fila %d faltan %r'%(rid,missing)
    print('fila %d OK'%rid)
font.byc={}
for g in range(font.n):
    u=struct.unpack_from('<I',font.p3,HDR+g*36)[0]; font.byc.setdefault(u,g)
for ch in CHARS: assert ord(ch) in font.byc

new={}
for fid,data in ((1,bytes(font.p1)),(2,bytes(p2)),(3,bytes(font.p3)),(4,bytes(font.tex))):
    f=font.rows[fid]; plain=bytes(data)
    new[fid]=(font.cf.cipher(f,plain),len(plain))
blob=build_ordered(ORIG,new)
open(OUT,'wb').write(blob)
c2=load(OUT)
for rr in c2.rows: assert rr['ex']==len(c2.plain(rr))
print('escrito',OUT,len(blob),'verificado')
