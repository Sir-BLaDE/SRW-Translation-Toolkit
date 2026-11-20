# -*- coding: utf-8 -*-
import io,json,sys,os
sys.path.insert(0,os.path.expanduser('~/tools_vm'));sys.path.insert(0,os.path.expanduser('~'))
import cpk_util,fastinf
cpk_util.inflate=fastinf.inflate
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
S=os.path.expanduser('~/mnt/srwv/')
name=sys.argv[1];SRC=S+f'backup/MtZkn_{name}_original.cpk';OUT=S+f'outputs/MtZkn_{name}_names_fixed.cpk'
NAMES=S+'datos/mtzkn_names_es.json'
TAGS=(b"CHFN",b"CHNN",b"PRDC",b"RBTN",b"RBN2",b"PLTN")
names=json.load(io.open(NAMES,encoding='utf-8'))
cf=load(SRC);new={};changed=trunc=0
for f in cf.rows:
    pt=bytearray(b^0x5E for b in cf.plain(f));L=len(pt);pos=0
    while True:
        best=None
        for t in TAGS:
            i=pt.find(t,pos)
            if i>=0 and (best is None or i<best[0]): best=(i,t)
        if best is None: break
        i,t=best;p=i+4
        if p>=L or pt[p+1:p+4]!=b"^^^": pos=i+4;continue
        ln=pt[p];st=p+4;en=st+ln
        if en>L: pos=i+4;continue
        try: txt=bytes(pt[st:en]).decode('utf-8')
        except UnicodeDecodeError: pos=i+4;continue
        es=names.get(txt)
        if es is None: pos=en;continue
        if isinstance(es,list):
            vv=es;es=vv[-1]
            for c in vv:
                if len(c.encode('utf-8'))<=ln: es=c;break
        if es==txt: pos=en;continue
        eb=es.encode('utf-8')
        if len(eb)>ln:
            w=es.split()
            while w and len(" ".join(w).encode('utf-8'))>ln: w.pop()
            es2=" ".join(w)
            if not es2: es2=es.encode('utf-8')[:ln].decode('utf-8','ignore')
            eb=es2.encode('utf-8')[:ln];trunc+=1;print('TRUNC',repr(txt),'->',repr(es2),ln)
        pt[st:en]=eb+b' '*(ln-len(eb));changed+=1;pos=en
    assert len(pt)==L
    new[f['id']]=(cf.cipher(f,bytes(b^0x5E for b in pt)),L)
blob=build_ordered(SRC,new);open(OUT,'wb').write(blob)
k=load(OUT)
print(name,'nombres',changed,'recortados',trunc,'tam ok',all(len(k.plain(r))==len(cf.plain(q)) for r,q in zip(k.rows,cf.rows)))
