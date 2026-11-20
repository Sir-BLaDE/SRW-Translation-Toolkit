# -*- coding: utf-8 -*-
# HUD de combate (BTLC/EN0/CMN00_PC.CPK): Attack/Defend/Evade/Return Attack/Cannot Attack, Counterattack..., Critical
import os,sys,struct
sys.path.insert(0,'/tmp/b')
from cpk_util import load
import numpy as np, cv2
from PIL import Image,ImageFilter
import effw
H=os.environ['HOME']; P=H+'/mnt/srwv/'
SRC=P+'backup/BTLC_EN0_CMN00_PC_original.cpk'
if not os.path.exists(SRC):
    import shutil; shutil.copy2(H+'/mnt/Super Robot Wars V/Data/BTLC/EN0/CMN00_PC.CPK',SRC)
c=load(SRC); R={r['id']:r for r in c.rows}
FI='/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf'
def get(i):
    d=c.plain(R[i]); h,w=struct.unpack('<II',d[12:20]); return d[:128],np.frombuffer(d[128:128+w*h*4],np.uint8).reshape(h,w,4).copy(),w,h
def lines(a,gap=3,x0=0):
    m=a[...,3]>8; rows=np.where(m.any(axis=1))[0]; g=[]; s=p=rows[0]
    for r in rows[1:]:
        if r-p>gap: g.append((s,p+1)); s=r
        p=r
    g.append((s,p+1)); out=[]
    for s,e in g:
        xs=np.where(m[s:e].any(axis=0))[0]; out.append((xs.min()-x0,s,xs.max()+1,e))
    return out
def smask(text,w,h,font=FI,shear=0.0,capfill=0.9,sx_max=1.15):
    m=effw.mask(text,w,h,font=font,capfill=capfill,sx_max=sx_max,sx_min=0.5)
    if shear: m=m.transform(m.size,Image.AFFINE,(1,shear,-shear*h/2,0,1,0),Image.BICUBIC)
    return m
def redo(a,box,text,font=FI,capfill=0.88,shear=0.0,width=None,pad=4,ol=5,spread=0):
    x0,y0,x1,y1=box; x0=max(x0,0);y0=max(y0,0);x1=min(x1,a.shape[1]);y1=min(y1,a.shape[0]); cx=(x0+x1)//2
    reg=a[y0:y1,x0:x1].copy(); op=reg[...,3]>200; lum=reg[...,:3].astype(int).sum(axis=2)
    thr=np.percentile(lum[op],55); n=y1-y0; cols=np.full((n,3),np.nan)
    for y in range(n):
        s=reg[y][(reg[y][...,3]>200)&(lum[y]>=thr)]
        if len(s): cols[y]=s[...,:3].mean(axis=0)
    ok=~np.isnan(cols[:,0]); j=np.where(ok)[0]
    for y in range(n):
        if not ok[y]: cols[y]=cols[j[np.abs(j-y).argmin()]]
    dk=reg[op&(lum<=np.percentile(lum[op],8))][...,:3].mean(axis=0)
    w=width or (x1-x0); W=w+2*pad; h=n
    m=smask(text,w,h-2*2,font=font,shear=shear,capfill=capfill)
    mm=Image.new('L',(W,h),0); mm.paste(m,(pad,2))
    fill=np.asarray(mm,float)/255
    olm=np.asarray(mm.filter(ImageFilter.MaxFilter(ol)).filter(ImageFilter.GaussianBlur(0.8)),float)/255
    out=np.zeros((h,W,4),float)
    fcol=np.broadcast_to(cols[:,None,:],(h,W,3)); ocol=np.broadcast_to(dk,(h,W,3))
    out[...,:3]=ocol*(1-fill[...,None])+fcol*fill[...,None]; out[...,3]=np.maximum(olm,fill)*255
    xs=cx-W//2; xe=xs+W
    a[y0:y1,max(0,x0-60):min(a.shape[1],x1+60)]=0 if False else a[y0:y1,max(0,x0-60):min(a.shape[1],x1+60)]
    a[y0:y1,x0:x1]=0
    xs=max(xs,0); xe=min(xe,a.shape[1]); a[y0:y1,xs:xe]=out[:,(xs-(cx-W//2)):(xe-(cx-W//2))].astype(np.uint8)
def cols_of(a,box):
    x0,y0,x1,y1=box; reg=a[y0:y1,x0:x1]; op=reg[...,3]>200; lum=reg[...,:3].astype(int).sum(axis=2)
    thr=np.percentile(lum[op],55); n=y1-y0; cols=np.full((n,3),np.nan)
    for y in range(n):
        s_=reg[y][(reg[y][...,3]>200)&(lum[y]>=thr)]
        if len(s_): cols[y]=s_[...,:3].mean(axis=0)
    ok=~np.isnan(cols[:,0]); j=np.where(ok)[0]
    for y in range(n):
        if not ok[y]: cols[y]=cols[j[np.abs(j-y).argmin()]]
    dk=reg[op&(lum<=np.percentile(lum[op],8))][...,:3].mean(axis=0)
    return cols,dk
def redo2(a,box,text,capH,base,width,shear=0.18,font=FI,ol=5,centers=None,pad=6,thick=0):
    # box: banda (x0,y0,x1,y1); base: linea base absoluta (y); capH: altura de mayuscula; width: ancho maximo del texto
    from PIL import ImageDraw,ImageFont
    x0,y0,x1,y1=box; x0=max(x0,0);y0=max(y0,0);x1=min(x1,a.shape[1]);y1=min(y1,a.shape[0])
    cols,dk=cols_of(a,(x0,y0,x1,y1)); w=x1-x0; h=y1-y0
    sz=capH*2
    while sz>5:
        f=ImageFont.truetype(font,sz); bb=f.getbbox('H')
        if bb[3]-bb[1]<=capH: break
        sz-=1
    lay=Image.new('L',(w*3,h),0); d=ImageDraw.Draw(lay); by=base-y0
    if centers:
        for ch,cxp in zip(text,centers):
            if ch==' ': continue
            tb=f.getbbox(ch,anchor='ls'); d.text((w+cxp-x0-(tb[0]+tb[2])/2,by),ch,font=f,fill=255,anchor='ls')
        tm=lay.crop((w,0,2*w,h))
    else:
        tb=f.getbbox(text,anchor='ls'); tw=tb[2]-tb[0]
        d.text((w*1.5-(tb[0]+tb[2])/2,by),text,font=f,fill=255,anchor='ls')
        tm=lay.crop((w//2*0+int(w*1.5-w/2),0,int(w*1.5+w/2),h)) if False else lay.crop((w,0,2*w,h))
        arr=np.asarray(lay); xs=np.where(arr.max(axis=0)>0)[0]; tw=xs.max()-xs.min()+1; cx=(xs.max()+xs.min())/2
        if tw>width: # comprime horizontalmente alrededor del centro
            sc=width/tw; seg=lay.crop((int(xs.min()),0,int(xs.max())+1,h)); seg=seg.resize((max(1,int(tw*sc)),h),Image.LANCZOS)
            lay2=Image.new('L',(w*3,h),0); lay2.paste(seg,(int(w*1.5-seg.size[0]/2),0)); tm=lay2.crop((w,0,2*w,h))
        else: tm=lay.crop((int(round(cx-w/2)),0,int(round(cx-w/2))+w,h))
    if shear: tm=tm.transform(tm.size,Image.AFFINE,(1,shear,-shear*by,0,1,0),Image.BICUBIC)
    if thick: tm=tm.filter(ImageFilter.MaxFilter(thick))
    mm=np.asarray(tm,float)/255
    olm=np.asarray(tm.filter(ImageFilter.MaxFilter(ol)).filter(ImageFilter.GaussianBlur(0.8)),float)/255
    out=np.zeros((h,w,4),float); fcol=np.broadcast_to(cols[:,None,:],(h,w,3)); ocol=np.broadcast_to(dk,(h,w,3))
    out[...,:3]=ocol*(1-mm[...,None])+fcol*mm[...,None]; out[...,3]=np.maximum(olm,mm)*255
    a[y0:y1,x0:x1]=out.astype(np.uint8)
EDITS={}
T19=['Contraataque','Defensa de apoyo','Ataque de apoyo','Segundo ataque','Ataque combinado','Arma de mapa']
D19=[0,1,1,0,0,1]
T20=['Ataque','Defensa','Esquiva','Réplica',None,'No puede atacar']
def run():
    hd,a,W,Hh=get(19); L=lines(a); assert len(L)==6,L
    capH=L[0][3]-L[0][1]-6   # Counterattack sin descendentes: altura incluye contorno
    for b,t,dsc in zip(L,T19,D19):
        base=b[3]-(round(capH*0.26)+3 if dsc else 3)
        bw=min(int((b[2]-b[0])*1.12),W-16)
        redo2(a,(0,b[1]-4,W,b[3]+4),t,capH,base,bw)
    EDITS[19]=a
    hd,a,W,Hh=get(20); L=lines(a); assert len(L)==6,L
    capH=L[0][3]-L[0][1]-4
    for b,t in zip(L,T20):
        if t is None: continue
        base=b[3]-2
        bw=min(int((b[2]-b[0])*1.12),W-10)
        redo2(a,(0,b[1]-3,W,b[3]+3),t,capH,base,bw,ol=3)
    EDITS[20]=a
    hd,a,W,Hh=get(14)
    m=a[...,3]>8
    # componentes (letras) a la derecha de la flecha
    n,lab,st,cen=cv2.connectedComponentsWithStats(m.astype(np.uint8),8)[:4]
    comps=sorted([(st[i,0],st[i,0]+st[i,2],st[i,1],st[i,1]+st[i,3]) for i in range(1,n) if st[i,4]>20])
    ce=[ (c_[0]+c_[1])/2 for c_ in comps[1:]]
    print('comp critical',comps,ce); assert len(ce)==7
    redo2(a,(31,0,W,Hh),'Crítico',28,36,300,shear=0.16,centers=ce,ol=7,thick=3)
    EDITS[14]=a
def sheet():
    S=Image.new('RGB',(1300,720),(0,0,0)); x=0
    for i,s in ((19,2),(20,2),(14,2)):
        a=EDITS[i]; im=Image.fromarray(a[...,[2,1,0,3]],'RGBA'); bg=Image.new('RGBA',im.size,(80,80,100,255)); bg.alpha_composite(im)
        S.paste(bg.convert('RGB').resize((im.size[0]*s,im.size[1]*s),Image.NEAREST),(x if i!=14 else 0,0 if i!=14 else 600)); x+=im.size[0]*s+20
    S.save(P+'tmp_vis/cmn_new.png')
if __name__=='__main__': run(); sheet(); print(sorted(EDITS))
