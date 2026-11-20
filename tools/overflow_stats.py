import sys, re, struct, csv, json, os, statistics
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
cf=load(r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk')
rows={r['id']:r for r in cf.rows}; p3=cf.plain(rows[3]); HDR=40; W=4096; N=(len(p3)-HDR)//36
adv={}
for g in range(N):
    off=HDR+g*36; u=struct.unpack_from('<I',p3,off)[0]; fl=struct.unpack_from('<8f',p3,off+4)
    adv.setdefault(u,fl[5])
CTRL=re.compile(r'\\c\d|\\a\d\d|\$[A-Za-z]\w*|%[ds]')
def lines(s):
    s=CTRL.sub('',s)
    return re.split(r'\r?\n|\\n|\\r\\n|\n',s)
def w(s): return sum(adv.get(ord(c),20.0) for c in s)
def pct(vals,p): 
    v=sorted(vals); return v[int(len(v)*p)] if v else 0

pairs=[]
with open(r'C:/Dev/Default Project/srwv/datos/lineas_batalla_final.csv',encoding='utf-8-sig',newline='') as f:
    for r in csv.DictReader(f): pairs.append((r['en'],r['es'],r['id']))
for label,idx in [('EN',0),('ES',1)]:
    vals=[max((w(x) for x in lines(p[idx])),default=0) for p in pairs if p[idx]]
    print('BATTLE',label,'n',len(vals),'p50',pct(vals,.5),'p90',pct(vals,.9),'p95',pct(vals,.95),'p99',pct(vals,.99),'max',max(vals))
# candidates: ES line wider than EN p99
lim=pct([max((w(x) for x in lines(p[0])),default=0) for p in pairs],.99)
print('EN p99 limit',lim)
bad=[]
for en,es,k in pairs:
    if not es: continue
    m=max((w(x) for x in lines(es)),default=0)
    if m>lim: bad.append((m,k,en,es))
bad.sort(reverse=True)
print('battle ES lines > EN p99:',len(bad))
for m,k,en,es in bad[:30]: print('  %d [%s] EN=%r ES=%r'%(m,k,en[:50],es[:70]))
