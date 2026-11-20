# -*- coding: utf-8 -*-
import os,sys,re,hashlib
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));sys.path.insert(0,os.path.expanduser('~/tools_vm'))
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
from layout_map import ES
from layout_map_extra import EXTRA,ALT
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE=ROOT+'/outputs/LayoutData_es_v2.cpk'; OUT=ROOT+'/outputs/LayoutData_es_v3.cpk'
M=dict(ES);M.update(EXTRA)
cf=load(BASE);nf={};ok=skip=0;sk=[]
for r in cf.rows:
    pt=bytearray(cf.plain(r));n0=len(pt)
    for en,es in M.items():
        nd=en.encode();p=0
        while True:
            i=pt.find(nd,p)
            if i<0:break
            j=i+len(nd)
            if pt[j:j+1]!=b'\0' or (i>0 and pt[i-1] not in (0,10)): p=i+1;continue
            k=j
            while k<len(pt) and pt[k]==0:k+=1
            reg=k-i
            for v in ALT.get(en,[es]):
                b=v.encode()
                if len(b)+1<=reg: break
            else: b=None
            if b is None or len(b)+1>reg:
                skip+=1;sk.append((en,es,reg));p=i+1;continue
            pt[i:k]=b+b'\0'*(reg-len(b));ok+=1;p=i+len(b)
    assert len(pt)==n0
    nf[r['id']]=(cf.cipher(r,bytes(pt)),n0)
open(OUT,'wb').write(build_ordered(BASE,nf))
k=load(OUT);print('ok',ok,'skip',skip,all(k.rows[r['id']]['ex']==len(k.plain(k.rows[r['id']])) for r in k.rows),hashlib.sha256(open(OUT,'rb').read()).hexdigest()[:12])
for s in sk[:30]:print(s)
