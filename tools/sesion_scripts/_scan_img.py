import os,sys,collections
sys.path.insert(0,'/tmp/b')
from cpk_util import load
D=os.environ['HOME']+'/mnt/Super Robot Wars V/Data/'
f=sys.argv[1]; k=load(f if f.startswith('/') else D+f)
print(f,len(k.rows))
cnt=collections.Counter(); ex={}
for r in k.rows[:int(sys.argv[2]) if len(sys.argv)>2 else 400]:
    try:
        if r['ex']>40_000_000: cnt['big']+=1; continue
        p=k.plain(r)
    except Exception as e: cnt['err']+=1; continue
    m=p[:4]; key={b'DDS ':'DDS',b'\x89PNG':'PNG',b'BLTU':'BLTU'}.get(m,repr(m)); cnt[key]+=1; ex.setdefault(key,[]).append((r['id'],len(p)))
print(dict(list(cnt.items())[:12]))
for k2,v in list(ex.items())[:6]: print(k2,v[:8])
