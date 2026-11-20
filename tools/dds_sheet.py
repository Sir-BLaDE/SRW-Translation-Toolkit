import os,sys,struct
sys.path.insert(0,os.path.expanduser('~/tools_vm'));sys.path.insert(0,os.path.expanduser('~'));sys.path.insert(0,'/tmp/b')
import cpk_util,fastinf; cpk_util.inflate=fastinf.inflate
from cpk_util import load
from PIL import Image,ImageDraw
src,out,lo,hi=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]); cell=int(sys.argv[5]) if len(sys.argv)>5 else 200
c=load(src); rows=[r for r in c.rows if lo<=r['id']<hi]
cols=8; n=len(rows); sh=Image.new('RGB',(cols*cell,((n+cols-1)//cols)*(cell+14)),(40,40,55)); dr=ImageDraw.Draw(sh)
for k,r in enumerate(rows):
    x=(k%cols)*cell; y=(k//cols)*(cell+14)
    try:
        d=c.plain(r); H,W=struct.unpack('<II',d[12:20])
        if d[:4]!=b'DDS ' or struct.unpack('<I',d[88:92])[0]!=32: dr.text((x+3,y),f'{r["id"]} nodds',fill=(255,255,0)); continue
        im=Image.frombuffer('RGBA',(W,H),d[128:128+W*H*4],'raw','BGRA',0,1)
        bg=Image.new('RGBA',im.size,(70,70,90,255)); bg.alpha_composite(im); bg=bg.convert('RGB'); bg.thumbnail((cell-4,cell-4))
        sh.paste(bg,(x+2,y+14)); dr.text((x+3,y),f'{r["id"]} {W}x{H}',fill=(255,255,0))
    except Exception as e: dr.text((x+3,y),f'{r["id"]} err',fill=(255,0,0))
sh.save(out); print(n)
