import os,sys,re,glob
sys.path.insert(0,'/tmp/b')
from cpk_util import load
H=os.environ['HOME']+'/mnt/Super Robot Wars V/'
pats=[re.compile(x.encode(),re.I) for x in sys.argv[1:]]
fs=glob.glob(H+'CommonData/MtData/EN/*.cpk')+glob.glob(H+'CommonData/hiyama/*_E.cpk')+glob.glob(H+'Data/AIDDATA/EN/*.cpk')+glob.glob(H+'Data/KURODATA/*/*.cpk')+glob.glob(H+'Data/KURODATA/*.cpk')+glob.glob(H+'CommonData/KuroData/*.cpk')+glob.glob(H+'Data/TABATA/EN/*.cpk')
for f in fs:
    if '/JP/' in f or '/HG/' in f or '/CN/' in f or '/HK/' in f or '/TW/' in f or os.path.getsize(f)>30_000_000: continue
    try:k=load(f)
    except Exception: continue
    for r in k.rows:
        if r['ex']>20_000_000: continue
        try:p=k.plain(r)
        except Exception: continue
        for pt in pats:
            for m in list(pt.finditer(p))[:3]:
                print(os.path.basename(f),r['id'],hex(m.start()),p[max(0,m.start()-50):m.start()+70],flush=True)
