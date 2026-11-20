import os,sys,re
sys.path.insert(0,'/tmp/b')
from cpk_util import load
D=os.environ['HOME']+'/mnt/Super Robot Wars V/'
pats=[p.encode() for p in sys.argv[2:]]
f=sys.argv[1]
k=load(f if f.startswith('/') else D+f)
for r in k.rows:
    if r['ex']>60_000_000: continue
    try:p=k.plain(r)
    except Exception: continue
    for pt in pats:
        for m in re.finditer(re.escape(pt),p):
            print(f.split('/')[-1],r['id'],hex(m.start()),p[max(0,m.start()-30):m.start()+40])
            break
