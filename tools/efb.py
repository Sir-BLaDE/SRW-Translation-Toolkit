import os,sys,time
sys.path.insert(0,os.path.expanduser('~/mnt/srwv/tools'))
import efm,cpk_util as U
from PIL import Image
import numpy as np
c=efm.load(efm.EFF);refs=efm.refs_of(c)
os.makedirs(os.path.expanduser('~/blobs'),exist_ok=True)
for i in map(int,sys.argv[1:]):
    t=time.time()
    r=[x for x in c.rows if x['id']==i][0]
    assert r['ex']==8294528
    hd,a=efm.rows_img(c,i)
    typ,d,n,res=efm.process(hd,a,refs)
    nb=hd+res.tobytes()
    assert len(nb)==r['ex']
    blob=U.compress(U.encrypt_data(nb))
    open(os.path.expanduser(f'~/blobs/eff_{i}.bin'),'wb').write(blob)
    open(os.path.expanduser(f'~/blobs/eff_{i}.raw'),'wb').write(nb)
    Image.fromarray(res[...,[2,1,0]]).resize((480,270)).save(os.path.expanduser(f'~/blobs/eff_{i}.png'))
    print(i,typ,round(d,1),n,len(blob),round(time.time()-t),flush=True)
