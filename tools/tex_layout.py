import os,sys,hashlib
sys.path.insert(0,'/tmp/b')
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
H=os.environ['HOME']; P=H+'/mnt/srwv/'
BASE=P+'backup/LayoutImage_original_20261118.cpk'
FONT='/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyrebonum-bold.otf'
c=load(BASE); rows={r['id']:r for r in c.rows}
A={i:np.frombuffer(c.plain(rows[i])[128:],dtype=np.uint8).reshape(1024,1024,4).copy() for i in rows}
HDR={i:c.plain(rows[i])[:128] for i in rows}
# etiquetas: (atlas, tipo, ventana(x0,y0,x1,y1) o semilla, texto)
LABELS=[
 ('Critical',0,'bg',(275,325,265,318,515,386),'¡Crítico!'),
 ('MainSub0',0,'bg',(291,150,285,92,708,180),'Princ. Sub'),
 ('MainSub1',1,'win',(165,0,578,88),'Princ. Sub'),
 ('MainSub3',3,'win',(140,163,440,224),'Princ. Sub'),
 ('MainSub3s',3,'win',(450,172,632,214),'Princ. Sub'),
 ('LvUp',3,'win',(135,518,345,578),'¡Sube Nv.!'),
 ('WeaponCaution',3,'win',(4,583,476,642),'¡Cuidado, arma!'),
 ('Pilot',3,'win',(430,903,562,958),'Piloto'),
]
SHR={'Score1':(0.84,1,lambda w,nw:0),'Score2':(0.84,1,lambda w,nw:0),'ExCnt2':(0.62,0.7,lambda w,nw:0)}
def box_of(l):
    n,k,t,s,txt=l; a=A[k]
    if t=='bg':
        col=a[s[1],s[0]]; m=np.all(a==col,axis=2); w_=np.zeros(m.shape,bool); w_[s[3]:s[5],s[2]:s[4]]=True; m&=w_; seen=np.zeros(m.shape,bool); st=[(s[0],s[1])]; seen[s[1],s[0]]=True
        while st:
            x,y=st.pop()
            for nx,ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                if 0<=nx<1024 and 0<=ny<1024 and m[ny,nx] and not seen[ny,nx]: seen[ny,nx]=True; st.append((nx,ny))
        ys,xs=np.where(seen); return (xs.min(),ys.min(),xs.max()+1,ys.max()+1),col
    x0,y0,x1,y1=s; sub=a[y0:y1,x0:x1,3]>0; ys,xs=np.where(sub)
    return (x0+xs.min(),y0+ys.min(),x0+xs.max()+1,y0+ys.max()+1),np.zeros(4,np.uint8)
def render(w,h,txt,bgcol,tkind):
    sw=3 if h>=40 else 2
    best=None
    for sz in range(h*2,5,-1):
        f=ImageFont.truetype(FONT,sz); bb=f.getbbox(txt,stroke_width=sw)
        if bb[2]-bb[0]<=w and bb[3]-bb[1]<=h: best=(f,bb);break
    f,bb=best
    lay=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(lay)
    x=(w-(bb[2]-bb[0]))//2-bb[0]; y=(h-(bb[3]-bb[1]))//2-bb[1]
    d.text((x,y),txt,font=f,fill=(255,255,255,255),stroke_width=sw,stroke_fill=(0,0,0,255))
    out=np.zeros((h,w,4),np.uint8); out[:]=bgcol
    L=np.array(lay).astype(float); al=L[...,3:4]/255
    rgb=L[...,:3][...,::-1]  # a BGR
    out[...,:3]=(rgb*al+out[...,:3].astype(float)*(1-al)).astype(np.uint8)
    out[...,3]=np.maximum(out[...,3],L[...,3].astype(np.uint8)) if bgcol[3]==0 else 255
    return out
TR=[lambda p:p,lambda p:p[:,::-1],lambda p:p[::-1],lambda p:p[::-1,::-1]]
def find(patch):
    res=[]; h,w=patch.shape[:2]
    rng=np.random.RandomState(1)
    for ti,T in enumerate(TR):
        pt=np.ascontiguousarray(T(patch))
        pk=lambda a:(a[...,0].astype(np.uint32)<<24)|(a[...,1].astype(np.uint32)<<16)|(a[...,2].astype(np.uint32)<<8)|a[...,3]
        P32=pk(pt)
        for k in A:
            A32=pk(A[k])
            best=None
            for _ in range(40):
                py,px=rng.randint(h),rng.randint(w); v=P32[py,px]
                cy,cx=np.where(A32==v)
                if best is None or len(cy)<len(best[0]): best=(cy,cx,py,px)
                if len(cy)<50: break
            cy,cx,py,px=best
            for y,x in zip(cy-py,cx-px):
                if y<0 or x<0 or y+h>1024 or x+w>1024: continue
                if np.array_equal(A32[y:y+h,x:x+w],P32): res.append((k,ti,x,y))
    return res
def main(apply):
    B={k:A[k].copy() for k in A}; log=[]
    for l in LABELS:
        (x0,y0,x1,y1),col=box_of(l); w,h=x1-x0,y1-y0
        patch=A[l[1]][y0:y1,x0:x1].copy()
        new=render(w,h,l[4],col,l[2])
        if l[0] in SHR:
            nw=int(w*SHR[l[0]][0]);hh=int(h*SHR[l[0]][1]);sm=render(nw,hh,l[4],col,l[2]);new=np.zeros((h,w,4),np.uint8);new[:]=col if l[2]=='bg' else 0;ox=SHR[l[0]][2](w,nw);oy=(h-hh)//2;new[oy:oy+hh,ox:ox+nw]=sm
        m=find(patch); print(l[0],(x0,y0,x1,y1),m)
        assert any(r[:2]==(l[1],0) and r[2:]==(x0,y0) for r in m)
        for (k,ti,x,y) in m:
            # inversas: flips son involuciones
            B[k][y:y+h,x:x+w]=TR[ti](new)
        log.append((l[0],new))
    return B,log
if __name__=='__main__':
    B,log=main(False)
    # vista previa
    for k in (0,3):
        im=Image.frombuffer('RGBA',(1024,1024),B[k].tobytes(),'raw','BGRA',0,1); bg=Image.new('RGBA',im.size,(70,70,90,255)); bg.alpha_composite(im); bg.convert('RGB').save(P+f'tmp_tex_prev_L{k}.png')
    np.save('/tmp/tx/B.npy',np.stack([B[i] for i in range(8)]))
