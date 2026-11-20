import os,sys,struct
sys.path.insert(0,os.path.expanduser('~/tools_vm'));sys.path.insert(0,os.path.expanduser('~'));sys.path.insert(0,'/tmp/b')
import cpk_util,fastinf; cpk_util.inflate=fastinf.inflate
from cpk_util import load
from PIL import Image
src=sys.argv[1]; ids=[int(x) for x in sys.argv[3:]]; out=sys.argv[2]
c=load(src); rows={r['id']:r for r in c.rows}
for i in ids:
    d=c.plain(rows[i]); H,W=struct.unpack('<II',d[12:20])
    im=Image.frombuffer('RGBA',(W,H),d[128:128+W*H*4],'raw','BGRA',0,1)
    bg=Image.new('RGBA',im.size,(70,70,90,255)); bg.alpha_composite(im)
    bg=bg.convert('RGB')
    if W>1000: bg=bg.resize((W//2,H//2))
    bg.save(f'{out}_{i}.png'); print(i,W,H)
