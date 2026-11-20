import os,sys,io,struct
sys.path.insert(0,'/tmp/b')
from cpk_util import load
from PIL import Image,ImageDraw
import numpy as np
H=os.environ['HOME']
f,a,b,out=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4]
T=int(sys.argv[5]) if len(sys.argv)>5 else 160
k=load(f if f.startswith('/') else H+'/mnt/Super Robot Wars V/Data/'+f)
cols=10 if T<=160 else 6; rows=k.rows[a:b]
S=Image.new('RGB',(T*cols,(T+12)*((len(rows)+cols-1)//cols)),(60,60,60)); d=ImageDraw.Draw(S)
for i,r in enumerate(rows):
    try:
        if r['ex']>12_000_000: raise Exception('big')
        p=k.plain(r)
        if p[:4]!=b'DDS ': raise Exception('nodds '+repr(p[:4]))
        h,w=struct.unpack('<II',p[12:20]); fc=p[84:88]
        if fc==b'\0\0\0\0' or len(p)==128+w*h*4:
            im=Image.fromarray(np.frombuffer(p[128:128+w*h*4],np.uint8).reshape(h,w,4)[:,:,[2,1,0,3]],'RGBA')
        else: im=Image.open(io.BytesIO(p)).convert('RGBA')
        bg=Image.new('RGBA',im.size,(90,90,90,255)); bg.alpha_composite(im); im=bg.convert('RGB'); im.thumbnail((T,T))
        S.paste(im,((i%cols)*T,(i//cols)*(T+12)+12)); d.text(((i%cols)*T+2,(i//cols)*(T+12)),'%d %dx%d'%(r['id'],w,h),fill=(255,255,0))
    except Exception as e:
        d.text(((i%cols)*T+2,(i//cols)*(T+12)),'%d %s'%(r['id'],str(e)[:14]),fill=(255,80,80))
S.save(H+'/mnt/srwv/tmp_vis/'+out)
