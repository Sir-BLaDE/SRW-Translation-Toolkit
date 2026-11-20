import os,sys,re
sys.path.insert(0,'/tmp/b')
from cpk_util import load
k=load(os.environ['HOME']+'/mnt/srwv/backup/STGEST_EN_original.cpk')
a,b=int(sys.argv[1]),int(sys.argv[2])
pat=re.compile(rb'\[\[Ito\r\n')
for r in k.rows[a:b]:
    p=k.plain(r)
    m=pat.search(p)
    if m: print(r['id'],p[m.start()-100:m.start()+250],flush=True)
