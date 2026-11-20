import os,sys,re
sys.path.insert(0,'/tmp/b')
from cpk_util import load
f=sys.argv[1]; a=int(sys.argv[2]); st=int(sys.argv[3])
k=load(os.environ['HOME']+'/mnt/Super Robot Wars V/'+f)
pats=[b'stowaway',b'Gamillan',b'all we know']
for r in k.rows[a::st]:
    if r['ex']>3_000_000: continue
    try:p=k.plain(r)
    except Exception: continue
    for pt in pats:
        i=p.find(pt)
        if i>=0: print(f,r['id'],pt,p[max(0,i-80):i+80],flush=True);break
print('DONE',a,flush=True)
