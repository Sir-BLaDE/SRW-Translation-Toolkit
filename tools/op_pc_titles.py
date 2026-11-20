import os,sys,struct,hashlib
sys.path.insert(0,'/tmp/b')
from cpk_util import load
import srwv_cpkbuild2 as B
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
H=os.environ['HOME'];P=H+'/mnt/srwv/'
G=H+'/mnt/Super Robot Wars V/Data/BTLC/EN0/OP_PC.CPK'
BK=P+'backup/BTLC_EN0_OP_PC_original.cpk'
if not os.path.exists(BK):
    import shutil; shutil.copy2(G,BK)
SRC=BK
T={0:'Traje móvil Crossbone Gundam: Skull Heart',1:'Sucesor Marciano Nadesico: La película – Príncipe de la Oscuridad',2:'Traje móvil Gundam: El contraataque de Char',3:'Daitarn 3, el invencible',
4:'Traje móvil Gundam 00: La película – El despertar del pionero',7:'Traje móvil Gundam: El destello de Hathaway',8:'Super Máquina Zambot 3',9:'Traje móvil Zeta Gundam',
10:'Mazinger Z: Edición Verdadera – ¡El Impacto!',11:'Traje móvil Gundam Unicorn',13:'Cross Ange: Rondo de ángeles y dragones',14:'Traje móvil Gundam ZZ',16:'Traje móvil Gundam SEED Destiny',
18:'Mazinger ZERO contra el Gran General de la Oscuridad'}
FONT='/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
def render(txt):
    sz=36
    while True:
        f=ImageFont.truetype(FONT,sz); bb=f.getbbox(txt,stroke_width=2)
        if bb[2]-bb[0]<=1240: break
        sz-=1
    lay=Image.new('RGBA',(1280,64),(0,0,0,0)); d=ImageDraw.Draw(lay)
    x=(1280-(bb[2]-bb[0]))//2-bb[0]; y=31-(bb[1]+bb[3])//2
    sh=Image.new('RGBA',(1280,64),(0,0,0,0)); ds=ImageDraw.Draw(sh)
    ds.text((x+2,y+2),txt,font=f,fill=(0,0,0,255),stroke_width=3,stroke_fill=(0,0,0,255)); sh=sh.filter(ImageFilter.GaussianBlur(1.5))
    d.text((x,y),txt,font=f,fill=(255,255,255,255),stroke_width=2,stroke_fill=(0,0,0,255))
    out=Image.alpha_composite(sh,lay); a=np.array(out)
    return a[:,:,[2,1,0,3]].copy(),sz
c=load(SRC); new={}; PT={}
for i,t in T.items():
    r=c.rows[i]; old=c.plain(r); assert old[:4]==b'DDS ' and len(old)==128+1280*64*4
    arr,sz=render(t); pt=old[:128]+arr.tobytes(); new[r['id']]=(c.cipher(r,pt),len(pt)); PT[r['id']]=pt; print(i,sz,t)
    if i in (1,10): Image.fromarray(arr[:,:,[2,1,0,3]],'RGBA').save(P+f'tmp_vis/op_new{i}.png')
os.makedirs('/tmp/to',exist_ok=True)
for f in os.listdir('/tmp/to'): os.remove('/tmp/to/'+f)
for rid,(ct,ex) in new.items():
    open('/tmp/to/row%d.bin'%rid,'wb').write(ct)
    open('/tmp/to/row%d.pt'%rid,'wb').write(PT[rid])
print('listo')
