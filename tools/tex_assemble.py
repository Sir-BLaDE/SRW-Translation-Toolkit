import os,sys,hashlib
sys.path.insert(0,'/tmp/b')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
P=os.environ['HOME']+'/mnt/srwv/'; BASE=P+'backup/LayoutImage_original_20261118.cpk'
c=load(BASE); new={}
for i in range(8):
    f=f'/tmp/tx/row{i}.bin'
    if os.path.exists(f): new[i]=(open(f,'rb').read(),len(open(f'/tmp/tx/row{i}.pt','rb').read()))
print(sorted(new))
out=P+'outputs/LayoutImage_EN_es_tex1.cpk'; blob=build_ordered(BASE,new); open(out,'wb').write(blob)
c2=load(out)
for r in c2.rows:
    pl=c2.plain(r); assert r['ex']==len(pl)
    if r['id'] in new: assert pl==open(f'/tmp/tx/row{r["id"]}.pt','rb').read()
    else: assert pl==c.plain([x for x in c.rows if x['id']==r['id']][0])
print('ok',len(blob),hashlib.sha256(blob).hexdigest()[:12])
