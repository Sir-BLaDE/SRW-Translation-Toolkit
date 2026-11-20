import os,sys,glob,time
sys.path.insert(0,'/tmp/b')
from cpk_util import load
G=os.environ['HOME']+'/mnt/Super Robot Wars V/'
N=[b'Return Attack',b'Counter Attack',b'Counterattack',b'PRESS START',b'Press any',b'Yamato Bridge']
N+=[n.decode().encode('utf-16le') for n in N]
files=sorted(set(glob.glob(G+'**/*.cpk',recursive=True)+glob.glob(G+'**/*.CPK',recursive=True)))
skip=sys.argv[1:]
for p in files:
    rel=p[len(G):]
    if os.path.getsize(p)>130e6 or any(s in rel for s in skip): continue
    try: c=load(p)
    except Exception as e: continue
    t=time.time(); hits={}
    for r in c.rows:
        if r['ex']>3_000_000: continue
        try: d=c.plain(r)
        except Exception: continue
        for n in N:
            k=d.count(n)
            if k: hits.setdefault(n.decode('utf-16le') if b'\x00' in n else n.decode(),[]).append((r['id'],k))
    if hits: print(rel,{k:v[:6] for k,v in hits.items()},flush=True)
