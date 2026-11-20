import os,sys,re,hashlib,shutil
sys.path.insert(0,'/tmp/b')
from cpk_util import load
import srwv_cpkbuild2 as B
H=os.environ['HOME'];P=H+'/mnt/srwv/'
G=H+'/mnt/Super Robot Wars V/Data/AIDDATA/EN/LayoutData.cpk'
shutil.copy2(G,P+'backup/LayoutData_instalado_antes_SPPE.cpk')
k=load(G); r=k.rows[0]; p=bytearray(k.plain(r)); n=0
def rep(a,b,old,new):
    global n
    seg=bytes(p[a:b]); out=bytearray(seg)
    for m in re.finditer(re.escape(old),seg):
        s=m.start()
        if old==b'SP' and s>0 and (65<=seg[s-1]<=90 or 97<=seg[s-1]<=122): continue
        out[s:s+len(new)]=new; n+=1
    p[a:b]=out
rep(0x73540,0x73580,b'SP',b'PE'); rep(0x79880,0x79bc0,b'SP',b'PE'); rep(0x7b920,0x7b980,b'SP',b'PE'); rep(0x8f160,0x8f180,b'SP',b'PE')
rep(0x7b920,0x7b980,b'Cost.PE',b'Cost.PE'); 
seg=bytes(p[0x7b920:0x7b980]); p[0x7b920:0x7b980]=seg.replace(b'Cost.PE',b'Cost.PE')
rep(0x79d40,0x79d70,b'Day',b'Dia')
print('cambios',n); assert len(p)==len(k.plain(r))
new={r['id']:(k.cipher(r,bytes(p)),len(p))}
out=P+'outputs/LayoutData_es_v7.cpk'
blob=B.build_ordered(G,new); open(out,'wb').write(blob)
k2=load(out); print([x['ex']==len(k2.plain(x)) for x in k2.rows], len(blob), os.path.getsize(G))
q=k2.plain(k2.rows[0]); print(q[0x7b930:0x7b950], q[0x79d52:0x79d62], q[0x79888:0x79898])
