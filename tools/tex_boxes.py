import numpy as np
def groups(a,y0,y1,x0,x1,gap=14,thr=8,mode='alpha'):
    s=a[y0:y1,x0:x1]
    m=(s[...,3]>thr) if mode=='alpha' else (s[...,:3].max(axis=2)>thr)
    cols=np.where(m.any(axis=0))[0]
    if len(cols)==0: return []
    out=[];st=cols[0];pr=cols[0]
    for c in cols[1:]:
        if c-pr>gap: out.append((st,pr));st=c
        pr=c
    out.append((st,pr))
    res=[]
    for a0,b0 in out:
        sub=m[:,a0:b0+1];ys=np.where(sub.any(axis=1))[0]
        res.append((x0+a0,y0+ys.min(),x0+b0+1,y0+ys.max()+1))
    return res
