import os,sys,re
sys.path.insert(0,'/tmp/b')
from cpk_util import load
pats=[x.encode() for x in sys.argv[3:]]
L=open('/tmp/lst.txt').read().split('\n')[int(sys.argv[1])::int(sys.argv[2])]
for f in L:
    if not f or os.path.getsize(f)>40_000_000: continue
    try:k=load(f)
    except Exception: continue
    for r in k.rows:
        if r['ex']>20_000_000: continue
        try:p=k.plain(r)
        except Exception: continue
        for pt in pats:
            for m in list(re.finditer(re.escape(pt),p))[:3]:
                print(f.split('Super Robot Wars V/')[-1],r['id'],hex(m.start()),p[max(0,m.start()-40):m.start()+60],flush=True)
