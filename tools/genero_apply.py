import os,sys,glob,shutil
sys.path.insert(0,os.environ['HOME']+'/mnt/srwv/tools'); sys.path.insert(0,'/tmp/b')
from cpk_util import load
import srwv_cpkbuild2 as B, genero_personajes as G
H=os.environ['HOME']; P=H+'/mnt/srwv/'; R=H+'/mnt/Super Robot Wars V/Data/'
def run(src,out):
    k=load(src); new={}; n=0
    for r in k.rows:
        try:t=k.plain(r).decode('utf8')
        except Exception: continue
        t2,ch=G.process(t)
        if t2!=t: new[r['id']]=(k.cipher(r,t2.encode()),len(t2.encode())); n+=len(ch)
    blob=B.build_ordered(src,new) if new else open(src,'rb').read()
    open(out,'wb').write(blob)
    k2=load(out); bad=[r['id'] for r in k2.rows if r['ex']!=len(k2.plain(r))]
    print(os.path.basename(src),n,'cambios',len(new),'filas bad',bad,flush=True)
    return n
which=sys.argv[1]
if which=='stg':
    os.makedirs(P+'outputs',exist_ok=True)
    run(R+'STAGE/STGEST_EN.CPK',P+'outputs/STGEST_EN_es_gen1.cpk')
else:
    os.makedirs(P+'outputs/dlc_es4',exist_ok=True)
    for f in sorted(glob.glob(P+'outputs/dlc_es3/dlc*_en.cpk')): run(f,P+'outputs/dlc_es4/'+os.path.basename(f))
