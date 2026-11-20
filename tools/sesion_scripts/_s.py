import os,sys,re
sys.path.insert(0,'/tmp/b')
from cpk_util import load
D=os.environ['HOME']+'/mnt/Super Robot Wars V/Data/STAGE/'
k=load(D+'STGEST_EN.CPK')
a,b=int(sys.argv[1]),int(sys.argv[2])
for r in k.rows[a:b]:
    try:p=k.plain(r)
    except Exception: continue
    for pt in (b'stowaway',b'humanoid weapon',b'Gamillan'):
        i=p.find(pt)
        if i>=0: print(r['id'],r['name'] if 'name' in r else '',pt,p[max(0,i-150):i+100],flush=True)
