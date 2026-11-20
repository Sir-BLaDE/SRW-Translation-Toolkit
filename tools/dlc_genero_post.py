import os,sys,re,glob,collections
sys.path.insert(0,'/tmp/b')
from cpk_util import load
import srwv_cpkbuild2 as B
H=os.environ['HOME']; P=H+'/mnt/srwv/'
SUB=[(r'\bpilotoo(s?)\b',r'piloto\1'),(r'\bPilotoo(s?)\b',r'Piloto\1'),
     (r'He echado el bronca','He recibido la bronca'),
     (r'\bCapitán (Katsuragi|Hoshino)\b',r'Capitana \1'),
     (r'\buna capitán\b','una capitana'),(r'\bUna capitán\b','Una capitana')]
os.makedirs(P+'outputs/dlc_es3',exist_ok=True)
for f in sorted(glob.glob(P+'outputs/dlc_es2/dlc*_en.cpk')):
    nme=os.path.basename(f); k=load(f); new={}; n=0
    for r in k.rows:
        p=k.plain(r)
        try:t=p.decode('utf8')
        except Exception: continue
        q=t
        for a,b in SUB: q,c=re.subn(a,b,q); n+=c
        if q!=t: new[r['id']]=(k.cipher(r,q.encode()),len(q.encode()))
    out=P+'outputs/dlc_es3/'+nme
    blob=B.build_ordered(f,new) if new else open(f,'rb').read()
    open(out,'wb').write(blob)
    k2=load(out); bad=[r['id'] for r in k2.rows if r['ex']!=len(k2.plain(r))]
    print(nme,n,'filas',len(new),'bad',bad,flush=True)
