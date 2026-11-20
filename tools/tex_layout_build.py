import os,sys,hashlib
sys.path.insert(0,'/tmp/b')
import numpy as np
import tex_layout as t
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
B,log=t.main(True)
c=t.c; new={}
for i in range(8):
    if np.array_equal(B[i],t.A[i]): continue
    pt=t.HDR[i]+B[i].tobytes(); assert len(pt)==len(c.plain(t.rows[i]))
    new[i]=(c.cipher(t.rows[i],pt),len(pt))
print('filas cambiadas',sorted(new))
out=t.P+'outputs/LayoutImage_EN_es_tex1.cpk'
blob=build_ordered(t.BASE,new); open(out,'wb').write(blob)
c2=load(out)
for r in c2.rows: assert r['ex']==len(c2.plain(r)),r['id']
for i in range(8):
    exp=(t.HDR[i]+B[i].tobytes()) if i in new else c.plain(t.rows[i])
    assert c2.plain([r for r in c2.rows if r['id']==i][0])==exp,i
print('ok',len(blob),hashlib.sha256(blob).hexdigest()[:12])
