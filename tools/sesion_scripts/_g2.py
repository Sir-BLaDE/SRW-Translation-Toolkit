import os,sys,re
sys.path.insert(0,'/tmp/b')
from cpk_util import load
pats=[b'stowaways',b's\0t\0o\0w\0a\0w\0a\0y\0s\0',b'Gamillans']
L=open('/tmp/lst.txt').read().split('\n')[int(sys.argv[1])::int(sys.argv[2])]
for f in L:
    if not f: continue
    try:k=load(f)
    except Exception as e: continue
    for r in k.rows:
        if r['ex']>40_000_000: continue
        try:p=k.plain(r)
        except Exception: continue
        for pt in pats:
            i=p.find(pt)
            if i>=0: print(f.split('Super Robot Wars V/')[-1],r['id'],hex(i),p[max(0,i-30):i+30]); break
