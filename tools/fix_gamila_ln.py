import os,sys,hashlib,shutil,re
sys.path.insert(0,'/tmp/b')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
H=os.environ['HOME']; P=H+'/mnt/srwv/'; G=H+'/mnt/Super Robot Wars V/'
src=G+'Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'; bk=P+'backup/antes_auditoria_20261119/KPACK_P4_LN_EN.CPK'
if not os.path.exists(bk): shutil.copy2(src,bk)
R=[(b'gamillanos',b'gamilas'),(b'gamillanas',b'gamilas'),(b'gamillana',b'gamila'),(b'gamillano',b'gamila'),(b'Gamillas',b'Gamilas')]
def fixpt(pt):
    pt=bytearray(pt); n=0
    for m in list(re.finditer(rb'[^\x00]+',bytes(pt))):
        s=m.group(0)
        if b'amill' not in s.lower(): continue
        t=s
        for o,r in R: t=t.replace(o,r)
        if t!=s:
            # el hueco total = string + nulos finales
            e=m.end()
            while e<len(pt) and pt[e]==0: e+=1
            assert len(t)<=len(s)
            pt[m.start():m.end()]=t+b'\x00'*(len(s)-len(t)); n+=1
    return bytes(pt),n
c=load(bk); new={}
for r in c.rows:
    pt=c.plain(r); np_,n=fixpt(pt)
    if n: assert len(np_)==len(pt); new[r['id']]=(c.cipher(r,np_),len(np_)); print('fila',r['id'],'cadenas',n)
out=P+'outputs/KPACK_P4_LN_EN_gamila.cpk'; blob=build_ordered(bk,new); open(out,'wb').write(blob)
k=load(out)
for r in k.rows: assert r['ex']==len(k.plain(r))
left=sum(k.plain(r).lower().count(b'gamillan')+k.plain(r).count(b'Gamillas') for r in k.rows)
print(len(blob),hashlib.sha256(blob).hexdigest()[:12],'restantes',left)
