import os,sys,re,glob
sys.path.insert(0,'/tmp/b')
from cpk_util import load
P=os.environ['HOME']+'/mnt/srwv/'
G=os.environ['HOME']+'/mnt/Super Robot Wars V/Data/DLCDIRE/EN/'
COMMON=re.compile(rb"\b(the|and|with|that|have|this|you|are|was|for|not|but|they|what|from|will|can|it's|I'm)\b")
tot=0;eng=0
for f in sorted(glob.glob(P+'outputs/dlc_es/dlc*_en.cpk')):
    n=os.path.basename(f); k=load(f); o=load(P+'backup/dlc_en/'+n)
    assert len(k.rows)==len(o.rows)
    t=e=0
    for r in k.rows:
        p=k.plain(r)
        for m in re.finditer(rb'\[\[[^\r\n]*\r\n((?:.|\r|\n)*?)\]\]',p):
            t+=1
            if len(COMMON.findall(m.group(1)))>=2: e+=1
    same=open(G+n,'rb').read()==open(P+'backup/dlc_en/'+n,'rb').read()
    tot+=t;eng+=e
    print(n,'bloques',t,'ingles',e,'juego==original',same,flush=True)
print(tot,eng)
