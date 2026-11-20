import os,sys,time,struct,json,subprocess,tempfile
sys.path.insert(0,os.path.expanduser('~/tools_vm'));sys.path.insert(0,os.path.expanduser('~'));sys.path.insert(0,'/tmp/b')
import cpk_util,fastinf; cpk_util.inflate=fastinf.inflate
from cpk_util import load
from PIL import Image, ImageOps
import numpy as np
src,out,lo,hi=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
c=load(src); t0=time.time(); done=set()
if os.path.exists(out):
    for l in open(out): done.add(json.loads(l)['id'])
f=open(out,'a')
for r in c.rows[lo:hi]:
    if r['id'] in done: continue
    if time.time()-t0>140: print('parcial hasta',r['id']);break
    try:d=c.plain(r)
    except Exception: continue
    if d[:4]!=b'DDS ': f.write(json.dumps({'id':r['id'],'t':'nodds'})+'\n');continue
    H,W=struct.unpack('<II',d[12:20]); bpp=struct.unpack('<I',d[88:92])[0]
    if bpp!=32 or W*H*4+128>len(d): f.write(json.dumps({'id':r['id'],'t':'fmt','w':W,'h':H,'bpp':bpp})+'\n');continue
    im=Image.frombuffer('RGBA',(W,H),d[128:128+W*H*4],'raw','BGRA',0,1)
    bg=Image.new('RGBA',im.size,(60,60,80,255)); bg.alpha_composite(im); g=bg.convert('L')
    if max(W,H)>2000: g=g.resize((W//2,H//2))
    p=tempfile.mktemp(suffix='.png'); ImageOps.invert(g).save(p)
    o=subprocess.run(['tesseract',p,'-','--psm','11','-l','eng'],capture_output=True,text=True).stdout
    os.remove(p)
    txt=' | '.join(x.strip() for x in o.split('\n') if sum(ch.isalpha() for ch in x)>=3)
    f.write(json.dumps({'id':r['id'],'w':W,'h':H,'t':txt[:400]},ensure_ascii=False)+'\n'); f.flush()
print('fin',round(time.time()-t0))
