import os,sys,struct
sys.path.insert(0,os.path.expanduser('~/tools_vm'));sys.path.insert(0,os.path.expanduser('~'))
import numpy as np, cv2
from PIL import Image,ImageDraw,ImageFont
import cpk_util,fastinf
cpk_util.inflate=fastinf.inflate
from cpk_util import load
EFF=os.path.expanduser('~/mnt/Super Robot Wars V/Data/ANIME/effwin.cpk')
FB='/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf'
if not os.path.exists(FB): FB='/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
HDR={'SOLAR':('SISTEMA SOLAR',385),'SPACE':('MAPA ESPACIAL',335),'WORLD':('MAPA MUNDIAL',335)}
REF={'SOLAR':522,'SPACE':528,'WORLD':531}
# key:(box x0,y0,x1,y1, text x0,x1, spanish)
LAB={
'solar':[(55,525,185,565,85,126,'SOL'),(375,762,500,795,392,459,'MERCURIO'),(500,755,600,785,511,559,'VENUS'),
 (605,742,715,775,623,687,'TIERRA'),(735,727,835,757,747,800,'MARTE'),(955,740,1095,772,973,1061,'JÚPITER'),
 (1200,672,1330,702,1218,1295,'SATURNO'),(1445,570,1575,600,1462,1538,'URANO'),(1745,515,1885,545,1762,1851,'NEPTUNO'),
 (1660,222,1775,252,1673,1737,'PLUTÓN')],
'galaxy':[(1575,580,1830,615,1599,1796,'VÍA LÁCTEA'),(385,825,720,860,416,687,'GRAN NUBE DE MAGALLANES')],
'earth':[(295,665,440,695,325,400,'TIERRA'),(1425,312,1555,342,1453,1513,'LUNA')]}
def salmon(a):
    R=a[...,0].astype(int);G=a[...,1].astype(int);B=a[...,2].astype(int)
    return (abs(R-255)<40)&(abs(G-137)<45)&(abs(B-126)<45)
def rows_img(c,i):
    r=[x for x in c.rows if x['id']==i][0];p=c.plain(r)
    return p[:128],np.frombuffer(p[128:],np.uint8)[:1920*1080*4].reshape(1080,1920,4).copy()
def htype(rgb,refs):
    cr=(150,20,580,90);best=None
    for k,v in refs.items():
        d=np.abs(rgb[20:90,150:580].astype(int)-v[20:90,150:580].astype(int)).mean()
        if best is None or d<best[0]: best=(d,k)
    return best
def draw_text(rgb,txt,x0,base,capH,maxw,fill,shadow,track=1.0,tmask=None):
    size=int(round(capH/0.716))
    f=ImageFont.truetype(FB,size)
    w0=sum(f.getlength(ch) for ch in txt)+track*(len(txt)-1)
    if w0>maxw:
        size=int(size*max(maxw/w0,0.88));f=ImageFont.truetype(FB,size)
    w=int(sum(f.getlength(ch) for ch in txt)+track*(len(txt)-1))+6
    lay=Image.new('L',(w+4,size*2),0);d=ImageDraw.Draw(lay);x=0
    for ch in txt:
        d.text((x,size*1.5),ch,font=f,fill=255,anchor='ls');x+=f.getlength(ch)+track
    if w>maxw:
        lay=lay.resize((max(1,int(lay.width*maxw/w)),lay.height),Image.LANCZOS)
    H,W=rgb.shape[:2]
    full=Image.new('L',(W,H),0);full.paste(lay,(int(x0),int(base-size*1.5)))
    m=np.array(full).astype(np.float32)/255
    sh=np.roll(np.roll(m,1,0),1,1)
    out=rgb.astype(np.float32)
    out=out*(1-sh[...,None]*0.85)+np.array(shadow,np.float32)[None,None]*sh[...,None]*0.85
    out=out*(1-m[...,None])+np.array(fill,np.float32)[None,None]*m[...,None]
    return np.clip(out,0,255).astype(np.uint8)
def do_labels(rgb,key,log=None):
    out=rgb.copy();n=0
    for (x0,y0,x1,y1,t0,t1,es) in LAB[key]:
        sub=salmon(out[y0:y1,x0:x1])
        rc=sub.sum(1)
        if rc.max()<25: continue
        yu=y0+int(rc.argmax())
        reg=salmon(out[y0:yu-1,t0-3:t1+3])
        ys,xs=np.where(reg)
        if len(ys)<10: continue
        ty0=y0+ys.min();ty1=y0+ys.max();tx0=t0-3+xs.min();tx1=t0-3+xs.max()
        capH=ty1-ty0+1
        capH={'MERCURIO':11,'VENUS':12}.get(es,15 if capH>=12 else capH)
        m=np.zeros(out.shape[:2],np.uint8)
        m[ty0-4:ty1+5,tx0-4:tx1+5]=1
        full=np.zeros(out.shape[:2],bool);full[y0:yu-1,t0-3:t1+3]=salmon(out)[y0:yu-1,t0-3:t1+3]
        mk=cv2.dilate((full*255).astype(np.uint8),np.ones((7,7),np.uint8))
        mk=cv2.bitwise_and(mk,m*255)
        out=cv2.inpaint(out,mk,3,cv2.INPAINT_TELEA)
        ul=yu  # underline row
        maxw=min(x1,tx0+ (np.where(salmon(out[yu:yu+1,x0:x1+60])[0])[0].max() if False else 0))
        # available width: up to underline end minus slashes
        uxs=np.where(sub[int(rc.argmax())])[0]
        avail=(x0+uxs.max())-34-tx0
        maxw=min(avail,(tx1-tx0)*1.06) if es!='GRAN NUBE DE MAGALLANES' else (tx1-tx0)*1.04
        out=draw_text(out,es,tx0,ty1+1,capH,maxw,(255,137,126),(25,8,18),track=1.0)
        n+=1
    return out,n
def do_header(rgb,typ):
    out=rgb.copy()
    R=rgb[...,0].astype(int);G=rgb[...,1].astype(int);B=rgb[...,2].astype(int)
    m=np.zeros(rgb.shape[:2],np.uint8)
    reg=((B>R+12)|((R+G+B)>420))[22:84,150:575]
    xe=575 if typ=='SOLAR' else 512
    reg=reg[:,:xe-150]
    m[22:84,150:xe]=reg
    m=cv2.dilate(m*255,np.ones((9,9),np.uint8))
    m[:,:150]=0;m[:,xe+3:]=0
    ys,xs=np.where(m>0)
    inp=cv2.inpaint(out,m,5,cv2.INPAINT_TELEA)
    txt,maxw=HDR[typ]
    # original caps: y range
    capH=int(np.where((B>R+12)[30:70,150:575].any(1))[0].max()-np.where((B>R+12)[30:70,150:575].any(1))[0].min()+1)
    size=int(round(capH/0.716)); x0=163
    while True:
        f=ImageFont.truetype(FB,size)
        nat=sum(f.getlength(ch) for ch in txt)
        tr=min(14,(maxw-nat)/(len(txt)-1))
        if tr>=2 or size<20: break
        size-=1
    base=30+int(np.where((B>R+12)[30:70,150:575].any(1))[0].max())+1
    H,W=rgb.shape[:2]
    lay=Image.new('L',(W,H),0);d=ImageDraw.Draw(lay);x=x0
    for ch in txt:
        d.text((x,base),ch,font=f,fill=255,anchor='ls');x+=f.getlength(ch)+tr
    mm=np.array(lay).astype(np.float32)/255
    sh=np.array(Image.fromarray((np.roll(np.roll(mm,2,0),2,1)*255).astype(np.uint8)).filter(__import__('PIL.ImageFilter',fromlist=['x']).GaussianBlur(1))).astype(np.float32)/255
    res=inp.astype(np.float32)
    res=res*(1-sh[...,None]*0.8)+np.array([20,18,30],np.float32)*sh[...,None]*0.8
    yy=np.arange(H)[:,None]
    t=np.clip((yy-(base-capH))/capH,0,1)
    top=np.array([215,242,250],np.float32);bot=np.array([105,165,195],np.float32)
    col=(top[None,None]*(1-t[...,None])+bot[None,None]*t[...,None])*np.ones((1,W,1),np.float32)
    res=res*(1-mm[...,None])+col*mm[...,None]
    return np.clip(res,0,255).astype(np.uint8)
def process(hd,a,refs):
    rgb=a[...,[2,1,0]].copy()
    d,typ=htype(rgb,refs)
    out=do_header(rgb,typ);n=0
    keys={'SOLAR':['solar'],'SPACE':['galaxy','earth'],'WORLD':[]}[typ]
    for k in keys:
        out,nn=do_labels(out,k);n+=nn
    res=a.copy();res[...,:3]=out[...,[2,1,0]]
    return typ,d,n,res
def refs_of(c):
    return {k:rows_img(c,v)[1][...,[2,1,0]] for k,v in REF.items()}
if __name__=='__main__':
    c=load(EFF);refs=refs_of(c)
    for i in map(int,sys.argv[1:]):
        hd,a=rows_img(c,i)
        typ,d,n,res=process(hd,a,refs)
        print(i,typ,round(d,1),n)
        Image.fromarray(res[...,[2,1,0]]).save(os.path.expanduser(f'~/mnt/srwv/tools/_m{i}.png'))
