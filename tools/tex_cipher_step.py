import os,sys,time
sys.path.insert(0,'/tmp/b')
import numpy as np
from cpk_util import load
H=os.environ['HOME']; P=H+'/mnt/srwv/'
c=load(P+'backup/LayoutImage_original_20261118.cpk'); rows={r['id']:r for r in c.rows}
B=np.load('/tmp/tx/B.npy')
i=int(sys.argv[1]); old=c.plain(rows[i]); hdr=old[:128]
A=np.frombuffer(old[128:],dtype=np.uint8).reshape(1024,1024,4)
if np.array_equal(A,B[i]): print(i,'sin cambios'); sys.exit()
pt=hdr+B[i].tobytes(); assert len(pt)==len(old)
t=time.time(); ct=c.cipher(rows[i],pt)
open(f'/tmp/tx/row{i}.bin','wb').write(ct); open(f'/tmp/tx/row{i}.pt','wb').write(pt)
print(i,'cifrado',len(ct),round(time.time()-t))
