import os,sys,time
sys.path.insert(0,os.path.expanduser('~/tools_vm'));sys.path.insert(0,os.path.expanduser('~'));sys.path.insert(0,'/tmp/b')
import cpk_util,fastinf; cpk_util.inflate=fastinf.inflate
from cpk_util import load
src,outd,lo,hi=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
os.makedirs(outd,exist_ok=True)
c=load(src); t=time.time(); n=0
print('filas',len(c.rows),flush=True)
for r in c.rows[lo:hi]:
    f=f'{outd}/{r["id"]}.bin'
    if os.path.exists(f): continue
    try: open(f,'wb').write(c.plain(r)); n+=1
    except Exception as e: pass
    if time.time()-t>150: print('parcial',r['id']);break
print('hecho',n,round(time.time()-t))
