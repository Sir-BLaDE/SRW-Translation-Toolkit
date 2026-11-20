import os,sys,re,json,glob,hashlib,collections
sys.path.insert(0,'/tmp/b')
from cpk_util import load
import srwv_cpkbuild2 as B
from nombres_ataques import R
from glosario_nombres3 import R3
H=os.environ['HOME']; P=H+'/mnt/srwv/'
M=dict(R);M.update(R3);M.pop('Full Cross',None)
SP=json.load(open('/tmp/spmap.json'))
patM=re.compile(r'(?<![\wáéíóúñÁÉÍÓÚÑ])('+'|'.join(re.escape(k) for k in sorted(M,key=len,reverse=True))+r')(?![\wáéíóúñ])')
patS=re.compile(r'(\[\[(?:　)*)('+'|'.join(re.escape(k) for k in sorted(SP,key=len,reverse=True))+r')(\r\n)')
GAM=[(r'\bGamillanos\b','Gamilas'),(r'\bgamillanos\b','gamilas'),(r'\bgamillanas\b','gamilas'),(r'\bGamillans\b','Gamilas'),(r'\bGamillan\b','gamila'),(r'\bGamillas\b','Gamilas')]
def fix(t,stat):
    def blk(m):
        s=m.group(0)
        s2=patS.sub(lambda x:x.group(1)+SP[x.group(2)]+x.group(3),s,count=1)
        if s2!=s: stat['sp']+=1
        s3=patM.sub(lambda x:M[x.group(1)],s2)
        if s3!=s2: stat['m']+=1
        return s3
    t=re.sub(r'\[\[.*?\]\]',blk,t,flags=re.S)
    for a,b in GAM:
        t,n=re.subn(a,b,t); stat['gam']+=n
    return t
only=sys.argv[1:] 
os.makedirs(P+'outputs/dlc_es2',exist_ok=True)
for f in sorted(glob.glob(P+'outputs/dlc_es/dlc*_en.cpk')):
    nme=os.path.basename(f)
    if only and nme not in only: continue
    k=load(f); new={}; stat=collections.Counter()
    for r in k.rows:
        p=k.plain(r)
        try: t=p.decode('utf8')
        except Exception: continue
        q=fix(t,stat).encode('utf8')
        if q!=p: new[r['id']]=(k.cipher(r,q),len(q))
    out=P+'outputs/dlc_es2/'+nme
    blob=B.build_ordered(f,new) if new else open(f,'rb').read()
    open(out,'wb').write(blob)
    k2=load(out); bad=[r['id'] for r in k2.rows if r['ex']!=len(k2.plain(r))]
    print(nme,dict(stat),'filas',len(new),'bad',bad,len(blob),flush=True)
