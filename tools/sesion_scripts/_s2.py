import os,sys,re
sys.path.insert(0,'/tmp/b')
from cpk_util import load
D=os.environ['HOME']+'/mnt/'
k=load(D+sys.argv[3])
a,b=int(sys.argv[1]),int(sys.argv[2])
pats=[re.compile(x) for x in (rb'all we know',rb'aboard now',rb'Yes, sir',rb'same thing',rb'Security until',rb'agile fighters')]
for r in k.rows[a:b]:
    p=k.plain(r)
    for pt in pats:
        m=pt.search(p)
        if m: print(r['id'],pt.pattern,p[max(0,m.start()-200):m.start()+100],flush=True);break
