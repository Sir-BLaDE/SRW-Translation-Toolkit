import os,sys,re,time,hashlib
sys.path.insert(0,os.path.expanduser('~/tools_vm'));sys.path.insert(0,os.path.expanduser('~'));sys.path.insert(0,'/tmp/b')
import cpk_util
import fastinf; cpk_util.inflate=fastinf.inflate
from cpk_util import load
import srwv_cpkbuild2 as B
from glosario_nombres3 import R3
from attacks import R
M=dict(R); M.update(R3)
del M['Full Cross']
keys=sorted(M,key=len,reverse=True)
PAT=re.compile(rb'(?<![A-Za-z0-9\xc3])('+b'|'.join(re.escape(k.encode()) for k in keys)+rb')(?![A-Za-z0-9])')
SRC=os.path.expanduser('~/mnt/Super Robot Wars V/Data/STAGE/STGEST_EN.CPK')
OUT=os.path.expanduser('~/mnt/srwv/outputs/STGEST_EN_es_v6.cpk')
c=load(SRC); new={}; tot=0
for r in c.rows:
    try: p=c.plain(r)
    except Exception: continue
    n=len(PAT.findall(p))
    if not n: continue
    q=PAT.sub(lambda m:M[m.group(1).decode()].encode(),p)
    new[r['id']]=(c.cipher(r,q),len(q)); tot+=n
print('filas',len(new),'reemplazos',tot,flush=True)
blob=B.build_ordered(SRC,new); open(OUT,'wb').write(blob)
c2=load(OUT)
bad=[r['id'] for r in c2.rows if r['ex']!=len(c2.plain(r))]
print('ex_mismatch',bad,len(blob),hashlib.sha256(blob).hexdigest()[:12],flush=True)
