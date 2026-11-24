# -*- coding: utf-8 -*-
"""Escanea DSC2 en ingles de MtZkn_{Nm,Pt,Rt}: identicos a DSCR original (copiables) vs distintos (traducir)."""
import os,struct,re,sys,json
from cpk_util import load
B=os.path.expanduser('~/mnt/srwv/backup/'); G=os.path.expanduser('~/mnt/Super Robot Wars V/CommonData/MtData/EN/')
X=lambda b:bytes(v^0x5E for v in b)
def fields(q):
    o={}
    for tag in (b'DSCR',b'DSC2'):
        i=q.find(tag)
        if i>=0: o[tag]=(i+8,struct.unpack('<H',q[i+4:i+6])[0])
    return o
EN=re.compile(r'\b(the|and|with|was|were|that|his|her|its|which|from|after|during)\b')
ES=re.compile(r'\b(el|la|los|las|de|del|que|con|una|un|su|sus|por|para)\b')
def scan(n):
    o=load(B+f'MtZkn_{n}_original.cpk'); c=load(G+f'MtZkn_{n}.cpk')
    oi={r['id']:r for r in o.rows}; res=[]
    for r in c.rows:
        pc=X(c.plain(r)); po=X(o.plain(oi[r['id']])); fc=fields(pc); fo=fields(po)
        if b'DSC2' not in fc: continue
        s,l=fc[b'DSC2']; t=pc[s:s+l].decode('utf8','replace').lower()
        if len(EN.findall(t))<=len(ES.findall(t)): continue
        same = b'DSCR' in fo and re.sub(rb'\s+',b'',po[fo[b'DSCR'][0]:fo[b'DSCR'][0]+fo[b'DSCR'][1]])==re.sub(rb'\s+',b'',po[fo[b'DSC2'][0]:fo[b'DSC2'][0]+fo[b'DSC2'][1]])
        res.append((r['id'],l,fc[b'DSCR'][1] if b'DSCR' in fc else 0,same))
    return res
if __name__=='__main__':
    for n in ('Nm','Pt','Rt'):
        r=scan(n); print(n,'DSC2 en ingles:',len(r),'identicos a DSCR:',sum(x[3] for x in r),'a traducir:',sum(not x[3] for x in r),'chars a traducir:',sum(x[1] for x in r if not x[3]))
