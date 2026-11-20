"""font_patch3.py - reconstruccion correcta de los glifos espanoles.

Parte de la fuente ORIGINAL (sin parchear) y:
  * usa los acentos REALES de la propia fuente del juego: ´ (g866), ~ (g961),
    ¨ (g864), en vez de dibujados a mano;
  * copia las metricas (bearing/advance) de la letra base, para que el glifo
    no se desplace a la derecha ni se solape con la siguiente letra;
  * rota 180 grados '?' y '!' para ¿ y ¡ (antes solo se volteaban verticalmente,
    por eso ¿ se veia como ?);
  * parchea los DOS mapas (fila 1 = dialogos, fila 2 = UI/batalla).
"""
import os, struct, sys
from PIL import Image, ImageDraw
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
import font_patch as fp
from cpk_util import load
from srwv_cpkbuild2 import build_ordered

ORIG = r'C:/Dev/Default Project/srwv/backup/FontInfo_EN_original.cpk'
OUT  = r'C:/Dev/Default Project/srwv/outputs/FontInfo_es3.cpk'
W, HDR = 4096, 40

# codepoints de relleno que se reasignan (2 bytes, no usados) -> letras nuevas
REUSE = [0xE0, 0xE8, 0xF9, 0xE2, 0xEA, 0xEB, 0xEF, 0x178]  # à è ù â ê ë ï Ÿ
ADD   = [0xE1, 0xED, 0xFA, 0xF1, 0xC1, 0xD3, 0xDA, 0xCD]   # á í ú ñ Á Ó Ú Í
# letras que ya tenian registro de relleno
HAVE  = {'é':0xE9, 'É':0xC9, 'ó':0xF3, 'Í':0xCD, 'ü':0xFC, '¿':0xBF, '¡':0xA1}

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

def accent_img(ch):
    """Recorta el acento real de la fuente a su caja de tinta."""
    g=font.rec_of(ch)
    img=font.get(g).copy()
    bb=ink_bbox(img)
    return img.crop((bb[0],bb[1],bb[2]+1,bb[3]+1))

ACC_IMGS = {'acute':accent_img('´'), 'tilde':accent_img('~'), 'dia':accent_img('¨')}
print('acentos reales:', {k:v.size for k,v in ACC_IMGS.items()})

# --- construir cada glifo -------------------------------------------------
targets={}
reuse_it=iter(REUSE)
for ch,base,kind in GLYPHS:
    g=font.byc.get(ord(ch))
    if g is None:
        cp=next(reuse_it); g=font.byc[cp]
    targets[ch]=(g, ord(ch))

for ch,base,kind in GLYPHS:
    g,_=targets[ch]
    gb=font.rec_of(base)
    base_img=font.get(gb).copy()
    _, base_fl=font.rec(gb)
    base_bb=ink_bbox(base_img)
    img=base_img

    if kind=='invertido':
        # rotar 180° SOLO la caja de tinta, y volver a pegarla en su sitio
        x0,y0,x1,y1=base_bb
        crop=base_img.crop((x0,y0,x1+1,y1+1))
        crop=crop.transpose(Image.ROTATE_180)
        img=base_img.copy()
        blank=Image.new('L',img.size,0)
        blank.paste(crop,(x0,y0))
        # el fondo original ya se ha llevado: usar solo la copia rotada
        img=blank
    else:
        acc=ACC_IMGS[kind].copy()
        if base=='i':
            # quitar el punto de la i (filas 4..9)
            d=ImageDraw.Draw(img); d.rectangle([0,4,img.width-1,9],fill=0)
            top_y=4
        else:
            top_y=base_bb[1]
        # centrar el acento sobre la tinta de la letra
        cx=(base_bb[0]+base_bb[2])/2.0
        ax=int(round(cx-(acc.width-1)/2.0))
        # 2 px de separacion entre acento y letra
        ay=int(max(0, top_y-2-acc.height))
        img.paste(acc,(ax,ay))

    # metricas EXACTAS de la letra base (bearing y advance)
    _, fl=font.rec(g)
    fl[4]=base_fl[4]; fl[5]=base_fl[5]
    newbb=ink_bbox(img)
    fl[7]=float(newbb[2]+1)
    font.put(g,img)
    font.write_rec(g,ord(ch),fl)
    print(' %r g=%-4d base=%r b=%.0f a=%.0f ink=%.0f bb=%s' %
          (ch,g,base,fl[4],fl[5],fl[7],newbb))

# --- mapa fila 1: mismo esquema que font_patch.py ------------------------
p1=bytes(font.p1)
MAP_REMOVE=REUSE+[0xFF]
MAP_ADD=ADD+[0xF3]
for old,new in zip(MAP_REMOVE,MAP_ADD):
    ob=chr(old).encode('utf-8'); nb=chr(new).encode('utf-8')
    assert len(ob)==len(nb)==2 and p1.count(ob)==1, (hex(old),p1.count(ob))
    i=p1.index(ob); p1=p1[:i]+nb+p1[i+2:]
font.p1=bytearray(p1)

# --- mapa fila 2 (UI/batalla): cirilicos -> espanol ----------------------
R2_OLD=list('ЁЪЫЬЭЮЯёъыьэюя')
R2_NEW=list('áéíóúñÁÉÍÓÚü¿¡')
r=font.rows[2]; p2=bytearray(font.cf.plain(r))
h=[struct.unpack_from('<I',p2,i*4)[0] for i in range(12)]
a,b=h[6],h[7]
s=bytes(p2[a:b])
for old,new in zip(R2_OLD,R2_NEW):
    ob=old.encode('utf-8'); nb=new.encode('utf-8')
    assert len(ob)==len(nb)==2 and s.count(ob)==1, (old,s.count(ob))
    i=s.index(ob); p2[a+i:a+i+2]=nb

# --- verificacion ---------------------------------------------------------
CHARS=list('áéíóúñÁÉÍÓÚü¿¡')
for rid,data in [(1,bytes(font.p1)),(2,bytes(p2))]:
    hh=[struct.unpack_from('<I',data,i*4)[0] for i in range(12)]
    ss=data[hh[6]:hh[7]].decode('utf-8','ignore')
    missing=[c for c in CHARS if c not in ss]
    assert not missing, 'fila %d faltan %r'%(rid,missing)
    print('fila %d: todos los caracteres presentes'%rid)
# reconstruir indice despues de reasignar los uids
font.byc={}
for g in range(font.n):
    u=struct.unpack_from('<I',font.p3,HDR+g*36)[0]; font.byc.setdefault(u,g)
for ch in CHARS:
    assert ord(ch) in font.byc, 'sin registro %r'%ch

# --- previews ASCII -------------------------------------------------------
os.makedirs('C:/Dev/Default Project/srwv/tools/_font_render',exist_ok=True)
for ch in ['á','é','í','ñ','Á','É','ü','¿','¡']:
    g=font.byc[ord(ch)]
    fl=struct.unpack_from('<8f',font.p3,HDR+g*36+4)
    x=int(round(fl[0]*W)); y=int(round(fl[1]*W)); w=int(round(fl[2]*W)); h=int(round(fl[3]*W))
    print('=== %r'%ch)
    for yy in range(h):
        row=font.tex[(y+yy)*W+x:(y+yy)*W+x+w]
        print(''.join('#' if v>90 else ('+' if v>30 else '.') for v in row))

# --- reconstruir ----------------------------------------------------------
new={}
for fid,data in ((1,bytes(font.p1)),(2,bytes(p2)),(3,bytes(font.p3)),(4,bytes(font.tex))):
    f=font.rows[fid]; plain=bytes(data)
    new[fid]=(font.cf.cipher(f,plain),len(plain))
blob=build_ordered(ORIG,new)
open(OUT,'wb').write(blob)
print('escrito',OUT,len(blob))
c2=load(OUT)
for r in c2.rows:
    pt=c2.plain(r)
    assert r['ex']==len(pt)
print('verificado: ex == plain en todos los registros')
