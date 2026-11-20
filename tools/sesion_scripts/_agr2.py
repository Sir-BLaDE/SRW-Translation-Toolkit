import os,sys,re,collections
sys.path.insert(0,'/tmp/b')
from cpk_util import load
D=os.environ['HOME']+'/mnt/Super Robot Wars V/Data/'
files=sys.argv[1:]
c=collections.Counter()
ex={}
for f in files:
    k=load(D+f if not f.startswith('/') else f)
    for r in k.rows:
        if r['ex']>20_000_000: continue
        try:t=k.plain(r).decode('utf-8','ignore')
        except Exception: continue
        for m in re.finditer(r'\b(un|una|unos|unas|el|la|los|las|este|esta|cada|del)\s+([A-Za-zÁÉÍÓÚáéíóúñÑ\.]+)',t):
            key=(m.group(1).lower(),m.group(2).lower()); c[key]+=1
            ex.setdefault(key,(f.split('/')[-1],r['id'],t[max(0,m.start()-20):m.end()+20].replace('\n','|').replace('\x00','|')))
words=collections.defaultdict(dict)
for (a,w),n in c.items(): words[w][a]=n
for w,d in sorted(words.items()):
    g={'m':sum(v for a,v in d.items() if a in('un','el','los','unos','este','del')),'f':sum(v for a,v in d.items() if a in('una','la','las','unas','esta'))}
    if g['m'] and g['f']: print(w,d)
