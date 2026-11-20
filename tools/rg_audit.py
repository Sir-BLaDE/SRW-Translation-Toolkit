# -*- coding: utf-8 -*-
import os,sys,hashlib,shutil,re
sys.path.insert(0,'/tmp/b'); sys.path.insert(1,os.path.dirname(os.path.abspath(__file__)))
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
from rg_dlc1 import D
H=os.environ['HOME']; P=H+'/mnt/srwv/'
bk=P+'backup/KPACK_P4_RG_EN_original.cpk'
c=load(bk); new={}; miss=[]; unk=[]; done=0
r=[x for x in c.rows if x['id']==0][0]
pt=bytearray(c.plain(r)); n0=len(pt)
START=0x1abb
for m in list(re.finditer(rb'[^\x00]+\x00*',bytes(pt))):
    if m.start()<START: continue
    s=m.group(0); t=s.rstrip(b'\0')
    try:u=t.decode('utf8')
    except Exception: continue
    if not re.search(r'[A-Za-z]{2}',u) : continue
    reg=len(s)
    if u not in D: unk.append((hex(m.start()),u));continue
    ok=None
    for cnd in D[u]:
        nb=cnd.encode('utf8')
        if len(nb)+1<=reg: ok=nb;break
    if ok is None: miss.append((hex(m.start()),u,reg,[len(x.encode())+1 for x in D[u]]));continue
    pt[m.start():m.end()]=ok+b'\x00'*(reg-len(ok)); done+=1
assert len(pt)==n0
new[0]=(c.cipher(r,bytes(pt)),len(pt))
print('hechas',done)
for x in miss: print('NOCABE',x)
for x in unk: print('SINDIC',x)
out=P+'outputs/KPACK_P4_RG_EN_es1.cpk'; blob=build_ordered(bk,new); open(out,'wb').write(blob)
k=load(out)
for q in k.rows: assert q['ex']==len(k.plain(q))
print(len(blob),hashlib.sha256(blob).hexdigest()[:12])
