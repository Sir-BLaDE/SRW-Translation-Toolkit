import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
FONT='/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf'
def mask(text,w,h,font=FONT,capfill=0.96,sx_max=1.2,sx_min=0.55):
    # alto: texto en mayusculas ocupa h*capfill; ancho: ajustado por escalado horizontal
    sz=int(h*1.6)
    while sz>5:
        f=ImageFont.truetype(font,sz);bb=f.getbbox(text)
        if bb[3]-bb[1]<=h*capfill: break
        sz-=1
    f=ImageFont.truetype(font,sz);bb=f.getbbox(text)
    im=Image.new('L',(bb[2]-bb[0]+2,bb[3]-bb[1]+2),0);ImageDraw.Draw(im).text((1-bb[0],1-bb[1]),text,font=f,fill=255)
    tw,th=im.size;sx=min(max(w/tw,sx_min),sx_max)
    im=im.resize((max(1,int(tw*sx)),th),Image.LANCZOS)
    m=Image.new('L',(w,h),0);m.paste(im,((w-im.size[0])//2,(h-th)//2))
    return m
def put(a,box,text,style='flat',blur=0.0,pad=1,**kw):
    x0,y0,x1,y1=[int(v) for v in box];w,h=x1-x0,y1-y0
    reg=a[y0:y1,x0:x1].copy()
    bg=a[max(y0-1,0),max(x0-1,0)].copy() if style!='keepbg' else reg[0,0]
    lum=reg[...,:3].astype(int).sum(axis=2)*(reg[...,3]>0 if kw.get('alphafg',True) else 1)
    m=mask(text,w-2*pad,h-2*pad,**{k:v for k,v in kw.items() if k in('font','capfill','sx_max','sx_min')})
    mm=Image.new('L',(w,h),0);mm.paste(m,(pad,pad))
    if blur>0: mm=mm.filter(ImageFilter.GaussianBlur(blur))
    M=np.asarray(mm,float)[...,None]/255
    if blur>0: M=np.minimum(1,M*kw.get('gain',1.6))
    out=np.zeros((h,w,4),float)
    if style=='grad':
        # color por fila del original (pixeles opacos)
        cols=np.zeros((h,3));ok=np.zeros(h,bool)
        for y in range(h):
            r=reg[y];s=r[r[...,3]>200]
            if len(s): cols[y]=s[...,:3].mean(axis=0);ok[y]=True
        for y in range(h):
            if not ok[y]:
                j=np.where(ok)[0];cols[y]=cols[j[np.abs(j-y).argmin()]]
        fg=np.zeros((h,w,4));fg[...,:3]=cols[:,None,:];fg[...,3]=255
        bgc=np.zeros(4);bgc[:3]=cols[:,None,:].mean(axis=0).squeeze() if False else cols.mean(axis=0)
        out[...,:3]=cols[:,None,:];out[...,3]=M[...,0]*255
        a[y0:y1,x0:x1]=out.astype(np.uint8);return
    # flat: color = pixel mas brillante del original
    idx=np.unravel_index(lum.argmax(),lum.shape);fgc=reg[idx].astype(float)
    if 'fg' in kw and kw['fg'] is not None: fgc=np.array(kw['fg'],float)
    bgc=bg.astype(float)
    out=bgc[None,None,:]*(1-M)+fgc[None,None,:]*M
    a[y0:y1,x0:x1]=np.clip(out,0,255).astype(np.uint8)
