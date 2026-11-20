# -*- coding: utf-8 -*-
import os,sys,re,hashlib
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));sys.path.insert(0,os.path.expanduser('~/tools_vm'))
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
from layout_lines_es import LD
from layout_short_es import SH
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE=ROOT+'/outputs/LayoutData_es_v3.cpk';OUT=ROOT+'/outputs/LayoutData_es_v4.cpk'
cf=load(BASE);r0=cf.rows[0];pt=bytearray(cf.plain(r0));n0=len(pt)
cjk=re.compile(r'[　-鿿가-힯]')
done=0;fail=[];unk=set()
for m in list(re.finditer(rb'[^\x00]+\x00+',bytes(pt))):
    s=m.group(0);t=s.rstrip(b'\0')
    if b'\n' not in t: continue
    try:u=t.decode('utf8')
    except Exception: continue
    if cjk.search(u) or not re.search(r'[A-Za-z]{4}',u): continue
    out=[];ch=False
    for l in u.split('\n'):
        if l in LD:
            out.append(LD[l]);ch=ch or LD[l]!=l
        else:
            out.append(l)
            if re.search(r'[A-Za-z]{3}',l) and not re.fullmatch(r'W+(yg)?',l.strip()): unk.add(l)
    if not ch: continue
    nb='\n'.join(out).encode();reg=len(s)
    if len(nb)+1>reg:
        out2=[SH.get(l,LD.get(l,l)) for l in u.split('\n')]
        nb=('\n'.join(out2)).encode()
        if len(nb)+1>reg:
            fail.append((u,'\n'.join(out2),len(nb)+1,reg));continue
    pt[m.start():m.end()]=nb+b'\0'*(reg-len(nb));done+=1
assert len(pt)==n0
print('hechos',done,'no caben',len(fail),'sin traducir',sorted(unk))
for f in fail:print(f)
if not fail or '--force' in sys.argv:
    nf={}
    for r in cf.rows:
        p=bytes(pt) if r['id']==0 else cf.plain(r)
        nf[r['id']]=(cf.cipher(r,p),len(p))
    open(OUT,'wb').write(build_ordered(BASE,nf));k=load(OUT)
    print('verif',all(k.rows[i]['ex']==len(k.plain(k.rows[i])) for i in range(len(k.rows))),hashlib.sha256(open(OUT,'rb').read()).hexdigest()[:12])
