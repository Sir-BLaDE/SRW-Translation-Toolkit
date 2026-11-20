# -*- coding: utf-8 -*-
"""prologue_translate3.py - reemplazo in-place con extractor v2 (meta=slot-22)."""
import sys, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
ORIG = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/Prologue.cpk'
OUT  = r'C:/Dev/Default Project/srwv/outputs/Prologue_es.cpk'
DATA = r'C:/Dev/Default Project/srwv/datos/prologue_full_v2.json'
TRANS= r'C:/Dev/Default Project/srwv/datos/prologue_trans_v3.json'
META = 22
d = json.load(open(DATA, encoding='utf-8'))
T = json.load(open(TRANS, encoding='utf-8'))

def fit(es, maxbytes):
    b=es.encode('utf-8')
    if len(b)<=maxbytes: return es, True
    words=es.split()
    while words and len(' '.join(words).encode('utf-8'))>maxbytes: words.pop()
    out=' '.join(words)
    if len(out.encode('utf-8'))>maxbytes:
        out=out.encode('utf-8')[:maxbytes].decode('utf-8','ignore')
    return out, False

def slot_strings(b, meta_start):
    out=[]; i=0
    while i < meta_start:
        j=b.find(b'\x00', i, meta_start)
        if j<0: break
        if j>i: out.append((i,j,b[i:j].decode('utf-8','ignore')))
        i=j+1
    return out

c=load(ORIG)
newrows={}
stats={'ok':0,'shrunk':0,'missing':0,'samples':[]}
for r in c.rows:
    pt=bytearray(c.plain(r)); rid=str(r['id']); rd=d.get(rid)
    if not rd:
        newrows[r['id']]=(c.cipher(r,bytes(pt)),len(pt)); continue
    cnt=rd['count']; slot=rd['slot']; meta=slot-META
    for si in range(cnt):
        base=24+si*slot
        b=bytes(pt[base:base+slot])
        spans=slot_strings(b, meta)
        for idx,(a,z,txt) in enumerate(spans):
            key=txt.strip()
            if key not in T or not T[key].strip():
                stats['missing']+=1; continue
            next_start = spans[idx+1][0] if idx+1<len(spans) else meta
            maxbytes = next_start - a - 1
            es,ok=fit(T[key].strip(), maxbytes)
            nb=bytearray(maxbytes+1)
            eb=es.encode('utf-8'); nb[:len(eb)]=eb
            pt[base+a:base+next_start]=nb
            if ok: stats['ok']+=1
            else:
                stats['shrunk']+=1
                if len(stats['samples'])<25:
                    stats['samples'].append((key,T[key],es,maxbytes))
    newrows[r['id']]=(c.cipher(r,bytes(pt)),len(pt))
print('stats:',{k:v for k,v in stats.items() if k!='samples'})
for s in stats['samples']: print('  RECORTADA: %r -> %r -> %r (max %d)'%s)
blob=build_ordered(ORIG,newrows)
open(OUT,'wb').write(blob)
c2=load(OUT)
for rr in c2.rows: assert rr['ex']==len(c2.plain(rr)), rr
print('escrito',OUT,len(blob),'verificado')
