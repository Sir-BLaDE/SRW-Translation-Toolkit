import os,sys,re,glob,collections
sys.path.insert(0,'/tmp/b')
from cpk_util import load
G=os.environ['HOME']+'/mnt/Super Robot Wars V/'
files=[p for p in glob.glob(G+'**/*',recursive=True) if p.lower().endswith('.cpk') and os.path.getmtime(p)>1.7948e9 or 'STGEST' in p or 'KPACK_P4_LN' in p or p.endswith('Prologue.cpk')]
rx=re.compile(rb'[\w\xc3\x80-\xc3\xbf]{0,12}[Gg]amil+[\w\xc3\x80-\xc3\xbf]*',re.I)
for p in sorted(set(files)):
    if 'LanguageData/' in p and '/EN/' not in p: continue
    if os.path.getsize(p)>120e6: continue
    try:c=load(p)
    except Exception as e: print('ERR',p,e);continue
    cnt=collections.Counter()
    for r in c.rows:
        if r['ex']>6_000_000: continue
        try:d=c.plain(r)
        except Exception: continue
        for m in rx.finditer(d): cnt[m.group(0)]+=1
    if cnt: print(p[len(G):],dict(cnt),flush=True)
