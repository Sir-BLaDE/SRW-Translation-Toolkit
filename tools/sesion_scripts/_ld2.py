import os,sys,re,shutil
sys.path.insert(0,'/tmp/b')
from cpk_util import load
import srwv_cpkbuild2 as B
H=os.environ['HOME'];P=H+'/mnt/srwv/'
G=H+'/mnt/Super Robot Wars V/Data/AIDDATA/EN/LayoutData.cpk'
shutil.copy2(G,P+'backup/LayoutData_instalado_antes_salvar.cpk')
k=load(G); r=k.rows[0]; p=bytearray(k.plain(r))
for old,new in ((b'Grab.',b'Salvar'),(b'Carga',b'Cargar')):
    for m in re.finditer(b'\x00'+re.escape(old)+b'\x00',bytes(p)):
        s=m.start()+1; nxt=p[s+len(old)+1]
        print(old,hex(s),'siguiente byte',hex(nxt),bytes(p[s+len(old)+1:s+len(old)+8]))
        assert nxt>=0x80 or nxt==0, 'no seguro'
        if nxt==0: print('  (omitido: no es el boton)'); continue
        p[s:s+len(new)+1]=new+b'\x00'
data=bytes(p); out=P+'outputs/LayoutData_es_v8.cpk'
blob=B.build_ordered(G,{r['id']:(k.cipher(r,data),len(data))}); open(out,'wb').write(blob)
k2=load(out); print([x['ex']==len(k2.plain(x)) for x in k2.rows],len(blob),os.path.getsize(G))
