import os,sys,shutil
sys.path.insert(0,'/tmp/b')
from cpk_util import load
import srwv_cpkbuild2 as B
H=os.environ['HOME'];P=H+'/mnt/srwv/'
G=H+'/mnt/Super Robot Wars V/Data/STAGE/STGEST_EN.CPK'
shutil.copy2(G,P+'backup/STGEST_EN_instalado_antes_concordancia.cpk')
k=load(G); r=[x for x in k.rows if x['id']==189][0]; p=k.plain(r)
old='¡Hay un clase Galleon!」'.encode(); new=('¡Hay un Galleon!'+' '*6+'」').encode()
assert len(old)==len(new) and p.count(old)==1,(len(old),len(new),p.count(old))
d=p.replace(old,new)
out=P+'outputs/STGEST_EN_es_conc1.cpk'
blob=B.build_ordered(G,{189:(k.cipher(r,d),len(d))}); open(out,'wb').write(blob)
k2=load(out); print(all(x['ex']==len(k2.plain(x)) for x in k2.rows),len(blob),os.path.getsize(G))
