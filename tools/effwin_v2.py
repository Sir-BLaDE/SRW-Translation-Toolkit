import os,sys,struct,hashlib
sys.path.insert(0,os.path.expanduser('~/tools_vm'));sys.path.insert(0,os.path.expanduser('~'));sys.path.insert(0,'/tmp/b')
import cpk_util as U,fastinf; U.inflate=fastinf.inflate
from cpk_util import load
import numpy as np, cv2
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import effw
G=os.path.expanduser('~/mnt/Super Robot Wars V');S=os.path.expanduser('~/mnt/srwv/')
SRC=S+'backup/effwin_instalado_antes_v2.cpk'
c=load(SRC);R={r['id']:r for r in c.rows}
FS='/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf'
FB='/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
FN=effw.FONT
def get(i):
    d=c.plain(R[i]);H,W=struct.unpack('<II',d[12:20]);return d[:128],np.frombuffer(d[128:128+W*H*4],np.uint8).reshape(H,W,4).copy(),W,H
def lines(a,gap=4):
    m=a[...,3]>8;rows=np.where(m.any(axis=1))[0];g=[];s=rows[0];p=rows[0]
    for r in rows[1:]:
        if r-p>gap: g.append((s,p+1));s=r
        p=r
    g.append((s,p+1));out=[]
    for s,e in g:
        xs=np.where(m[s:e].any(axis=0))[0];out.append((xs.min(),s,xs.max()+1,e))
    return out
def clear(a,b): x0,y0,x1,y1=b;a[y0:y1,x0:x1]=0
def outl(a,box,text,font=FN,capfill=0.9,grow=0,width=None):
    # texto relleno degradado por filas + contorno oscuro (alpha)
    x0,y0,x1,y1=box;cx=(x0+x1)//2
    if width: x0=cx-width//2;x1=x0+width
    x0-=grow;x1+=grow
    reg=a[box[1]:box[3],box[0]:box[2]]
    h=y1-y0;w=x1-x0
    # colores originales
    lum=reg[...,:3].astype(int).sum(axis=2);op=reg[...,3]>200
    ys=np.arange(reg.shape[0]);cols=np.zeros((reg.shape[0],3))
    thr=np.percentile(lum[op],55)
    for y in ys:
        s=reg[y][(reg[y][...,3]>200)&(lum[y]>=thr)]
        cols[y]=s[...,:3].mean(axis=0) if len(s) else np.nan
    okr=~np.isnan(cols[:,0])
    for y in ys:
        if not okr[y]: j=np.where(okr)[0];cols[y]=cols[j[np.abs(j-y).argmin()]]
    dk=reg[op&(lum<=np.percentile(lum[op],8))][...,:3].mean(axis=0)
    clear(a,box)
    m=effw.mask(text,w-6,h-6,font=font,capfill=capfill);mm=Image.new('L',(w,h),0);mm.paste(m,(3,3))
    fill=np.asarray(mm,float)/255
    ol=np.asarray(mm.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(0.8)),float)/255
    out=np.zeros((h,w,4),float)
    ci=np.clip(np.arange(h)*reg.shape[0]/h,0,reg.shape[0]-1).astype(int)
    ocol=np.broadcast_to(dk,(h,w,3)).copy();fcol=np.broadcast_to(cols[ci][:,None,:],(h,w,3))
    out[...,:3]=ocol*(1-fill[...,None])+fcol*fill[...,None];out[...,3]=np.maximum(ol,fill)*255
    t=a[y0:y1,x0:x1].astype(float);al=out[...,3:4]/255
    a[y0:y1,x0:x1]=np.clip(out*(1)+t*(1-al)*0,0,255).astype(np.uint8)
def flat(a,box,text,font=FS,capfill=0.78,fg=(255,255,255,255),width=None):
    x0,y0,x1,y1=box;cx=(x0+x1)//2
    if width: x0=cx-width//2;x1=x0+width
    h=y1-y0;w=x1-x0;clear(a,box)
    m=effw.mask(text,w,h,font=font,capfill=capfill,sx_max=1.0)
    M=np.asarray(m,float)/255
    out=np.zeros((h,w,4),np.uint8);out[...,:3]=fg[:3];out[...,3]=(M*fg[3]).astype(np.uint8)
    a[y0:y1,x0:x1]=out

EDITS={}
def rec(i,a): EDITS[i]=a
def run():
    # --- 94/96 fases
    for i in (94,96):
        h,a,W,H=get(i)
        effw.put(a,(14,186,292,224),'FASE ALIADA','grad');effw.put(a,(320,186,572,224),'FASE ENEMIGA','grad')
        effw.put(a,(12,244,292,286),'FASE ALIADA','flat',blur=2.2);effw.put(a,(318,244,574,286),'FASE ENEMIGA','flat',blur=2.2)
        rec(i,a)
    # --- 98 game over: DERROTA
    h,a,W,H=get(98)
    effw.put(a,(498,116,726,162),'DERROTA','flat',pad=0,capfill=0.95)
    effw.put(a,(736,106,968,158),'DERROTA','flat',blur=2.0,gain=1.4)
    effw.put(a,(646,172,882,222),'DERROTA','flat',blur=3.5,gain=1.1)
    # letras sueltas GAMEOVR -> D E R R O T A
    sol=[(2,230,23,265),(26,231,46,265),(50,231,71,265),(75,231,93,265),(97,230,118,265),(122,231,142,265),(147,231,166,265)]
    spc=[(180,224,213,271),(235,225,267,271),(291,225,326,271),(349,224,378,271),(403,224,436,271),(460,225,491,271),(516,224,548,271)]
    for b,ch in zip(sol,'DERROTA'): effw.put(a,b,ch,'flat',pad=0,capfill=0.98,sx_max=1.0)
    for b,ch in zip(spc,'DERROTA'): effw.put(a,b,ch,'flat',blur=2.0,gain=1.4,pad=3,capfill=0.9,sx_max=1.0)
    rec(98,a)
    # --- 6 y 7: etiquetas de combate / estados
    h,a,W,H=get(6)
    T6=['FALLO','¡CRÍTICO!','ESCUDO','BARRERA','ESQUIVA','CONTRA','APOYO ATQ','APOYO DEF','REATAQUE','ATQ COMBO']
    for (x0,y0,x1,y1),t in zip(lines(a),T6): outl(a,(x0,y0,x1,y1),t,width=max(x1-x0,118),capfill=0.92)
    rec(6,a)
    h,a,W,H=get(7)
    T7=['PODER ½','INMÓVIL','ÁNIMO ▼','PE ▼','EN ▼','MOVIL. ▼','PUNT. ▼','BLIND. ▼']
    for (x0,y0,x1,y1),t in zip(lines(a),T7): outl(a,(x0,y0,x1,y1),t,width=max(x1-x0,100),capfill=0.92,font='/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf')
    rec(7,a)
    # --- episodios
    SER=(621,638,655,673,682); 
    for i in (621,638,655,673,682,687,704,721,739,743):
        h,a,W,H=get(i);L=lines(a);font=FS if i in SER else FB
        res=[]
        for b in L:
            t=None
            x0,y0,x1,y1=b
            if W==768 and y0<20 and (x1-x0)<300 and i<687: t='JP'
            else: res.append(b)
        for b in L:
            x0,y0,x1,y1=b;h_=y1-y0
            # clasifica por posicion
            pass
        lab={ 'secret':'Episodio secreto','special':'Episodio especial','bonus':'Episodio extra','final':'Episodio final','plain':'Episodio'}
        # secuencia por fichero
        seq={621:['JP','special','secret'],638:['JP','special','secret'],655:['JP','special','secret'],673:['secret'],682:['bonus'],
             687:['plain','special','secret'],704:['plain','special','secret'],721:['plain','special','secret'],739:['secret'],743:['final']}[i]
        for b,k in zip(L,seq):
            x0,y0,x1,y1=b
            if k=='JP':
                # 第 [n] 話 -> "Ep." en la ranura izquierda, derecha vacia
                clear(a,b);flat(a,(17,10,123,103),'Ep.',font=font,capfill=0.8)
            else: flat(a,(x0,y0,x1,y1),lab[k],font=font,capfill=0.96)
        rec(i,a)
def sheet():
    for i,a in EDITS.items():
        im=Image.fromarray(a[...,[2,1,0,3]],'RGBA');bg=Image.new('RGBA',im.size,(70,70,90,255));bg.alpha_composite(im);bg=bg.convert('RGB')
        bg.save(S+f'tmp_vis/w_{i}.png')
pass

def title(a,box,text,font=FB,capfill=0.82):
    x0,y0,x1,y1=box;reg=a[y0:y1,x0:x1].copy()
    m0=(reg[...,0]>110)&(reg[...,0].astype(int)>reg[...,1].astype(int)+40)
    ys,xs=np.where(m0);bx0,bx1,by0,by1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
    lum=reg[...,:3].astype(int).sum(axis=2)
    cols=np.zeros((reg.shape[0],3));okr=np.zeros(reg.shape[0],bool)
    for y in range(by0,by1):
        sel=m0[y]&(lum[y]>=np.percentile(lum[m0],40))
        if sel.any(): cols[y]=reg[y][sel][:,:3].mean(axis=0);okr[y]=True
    for y in range(reg.shape[0]):
        if not okr[y]: j=np.where(okr)[0];cols[y]=cols[j[np.abs(j-y).argmin()]]
    m1=(reg[...,0].astype(int)>25)&(reg[...,0].astype(int)>reg[...,1].astype(int)+8)&(reg[...,0].astype(int)>reg[...,2].astype(int)+8)
    mk=cv2.dilate(m1.astype(np.uint8)*255,np.ones((24,9),np.uint8),anchor=(4,2))>0
    inp=reg[...,:3].astype(float).copy()
    for y in range(reg.shape[0]):
        row=mk[y]
        if not row.any(): continue
        xs=np.where(row)[0];l=xs.min();r=xs.max()
        lc=inp[y,max(l-8,0):max(l,1)].mean(axis=0) if l>0 else inp[y,r+1:r+9].mean(axis=0)
        rc=inp[y,r+1:r+9].mean(axis=0) if r<reg.shape[1]-1 else lc
        t=np.linspace(0,1,r-l+1)[:,None]
        seg=lc*(1-t)+rc*t
        inp[y,l:r+1]=np.where(row[l:r+1,None],seg,inp[y,l:r+1])
    inp=inp.astype(np.uint8)
    reg[...,:3]=inp
    w=bx1-bx0;h=by1-by0
    w2=int(max(w,len(text)*(h*0.62)));w2=min(w2,(x1-x0)-bx0-4)
    m=effw.mask(text,w2,h,font=font,capfill=capfill,sx_max=1.0)
    mm=Image.new('L',reg.shape[1::-1][0:2] if False else (reg.shape[1],reg.shape[0]),0);mm.paste(m,(bx0-int(np.where(np.asarray(m).max(axis=0)>20)[0][0]),by0))
    fill=np.asarray(mm,float)/255
    ol=np.asarray(mm.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.0)),float)/255
    dk=np.array([110,40,10.])
    f=cols[:,None,:]*np.ones((1,reg.shape[1],1))
    rgb=reg[...,:3].astype(float)
    rgb=rgb*(1-ol[...,None])+dk*ol[...,None]
    rgb=rgb*(1-fill[...,None])+f*fill[...,None]
    reg[...,:3]=np.clip(rgb,0,255).astype(np.uint8)
    a[y0:y1,x0:x1]=reg
def run2():
    for i,t,b in ((215,'Selección de sonido',(60,6,520,80)),(218,'Mensaje de interrupción',(20,6,680,84))):
        h,a,W,H=get(i);title(a,b,t);rec(i,a)
_old_main=None
if __name__=='__main__': run2();sheet();print(sorted(EDITS))
