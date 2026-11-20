"""font_match.py - busca la fuente del sistema mas parecida a la del juego
comparando las letras basicas (a,e,i,n,o,u) mediante IoU de mapas de bits.
"""
import sys,struct,glob,os
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from PIL import Image,ImageDraw,ImageFont

W,HDR=4096,40
p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf=load(p); rows={r['id']:r for r in cf.rows}
p3=cf.plain(rows[3]); tex=cf.plain(rows[4]); n=(len(p3)-HDR)//36
byc={}
for g in range(n):
    u=struct.unpack_from('<I',p3,HDR+g*36)[0]; byc.setdefault(u,g)

def game_ink(ch):
    g=byc[ord(ch)]; fl=struct.unpack_from('<8f',p3,HDR+g*36+4)
    x=int(round(fl[0]*W)); y=int(round(fl[1]*W)); w=int(round(fl[2]*W)); h=int(round(fl[3]*W))
    data=[v for yy in range(h) for v in tex[(y+yy)*W+x:(y+yy)*W+x+w]]
    img=Image.new('L',(w,h),0); img.putdata(data)
    return img.point(lambda v: 255 if v>90 else 0)

def crop_ink(img):
    bb=img.getbbox()
    return img.crop(bb) if bb else img

def to_bits(img,w,h):
    im=img.resize((w,h),Image.LANCZOS).point(lambda v: 1 if v>110 else 0)
    return list(im.getdata())

LETTERS='aenoiu'
targets={ch:crop_ink(game_ink(ch)) for ch in LETTERS}
print('tamano letras juego:',{ch:targets[ch].size for ch in LETTERS})

fonts=[]
for pat in ['C:/Windows/Fonts/*.ttf','C:/Windows/Fonts/*.otf','C:/Windows/Fonts/*.ttc']:
    fonts += glob.glob(pat)
# priorizar candidatos razonables
keys=['msgothic','YuGoth','arial','segoeui','calibri','tahoma','verdana','malgun','Futura','HelveticaNeue','Lato','Garamond','cambria','Consol','lucida','DejaVu']
fonts=[f for f in fonts if any(k.lower() in os.path.basename(f).lower() for k in keys)]
print('candidatos:',len(fonts))

results=[]
for fp in fonts:
    best=(0,None,None)
    for ttc_idx in ([0,1] if fp.lower().endswith('.ttc') else [0]):
        for size in range(22,40):
            try:
                font=ImageFont.truetype(fp,size,index=ttc_idx)
            except Exception:
                continue
            ious=[]
            ok=True
            for ch in LETTERS:
                try:
                    bbox=font.getbbox(ch)
                    tmp=Image.new('L',(size*2,size*2),0)
                    d=ImageDraw.Draw(tmp); d.text((size//2-size//4,size//2-size//4),ch,font=font,fill=255)
                    im=crop_ink(tmp)
                    tw,th=targets[ch].size
                    tb=to_bits(targets[ch],tw,th)
                    cb=to_bits(im,tw,th)
                    inter=sum(1 for a,b in zip(tb,cb) if a and b)
                    union=sum(1 for a,b in zip(tb,cb) if a or b)
                    ious.append(inter/union if union else 0)
                except Exception:
                    ok=False; break
            if ok:
                score=sum(ious)/len(ious)
                if score>best[0]: best=(score,size,ttc_idx)
    if best[0]>0:
        results.append((best[0],os.path.basename(fp),best[1],best[2]))
results.sort(reverse=True)
for score,name,size,idx in results[:25]:
    print(' %.4f  %-38s size=%d idx=%d'%(score,name,size,idx))
