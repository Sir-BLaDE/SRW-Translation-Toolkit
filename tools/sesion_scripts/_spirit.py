import os,sys,re,shutil,hashlib
sys.path.insert(0,'/tmp/b')
from cpk_util import load
import srwv_cpkbuild2 as B
H=os.environ['HOME'];P=H+'/mnt/srwv/'
G=H+'/mnt/Super Robot Wars V/CommonData/MtData/EN/rpw_jstr.cpk'
shutil.copy2(G,P+'backup/rpw_jstr_instalado_antes_espiritus.cpk')
k=load(G); r=k.rows[0]; p=k.plain(r)
PH={'Ajuste de puntería':'Puntería','Muro de Hierro':'Muro','Tiro Certero':'Certero'}
WHOLE={'Grit':'Brio','Rouse':'Ardor','Mercy':'Pena','Prospect':'Ilusión'}
out=bytearray(p); n=0; log=[]
i=0
while i<len(p):
    j=p.find(b'\x00',i)
    if j<0: j=len(p)
    if j>i:
        s=p[i:j].decode('utf8','replace') if True else ''
        try: s=p[i:j].decode('utf8')
        except Exception: i=j+1; continue
        z=j
        while z<len(p) and p[z]==0: z+=1
        avail=z-i-1
        t=WHOLE.get(s,s)
        for a,b in PH.items(): t=t.replace(a,b)
        if t!=s:
            nb=t.encode('utf8'); 
            if len(nb)>avail: print('NO CABE',s,t,len(nb),avail); i=j+1; continue
            out[i:i+avail]=nb+b'\x00'*(avail-len(nb)); n+=1; log.append((s[:50],t[:50]))
    i=j+1
print(n); [print(x) for x in log]
assert len(out)==len(p)
new={r['id']:(k.cipher(r,bytes(out)),len(out))}
o=P+'outputs/rpw_jstr_es_espiritus.cpk'
blob=B.build_ordered(G,new); open(o,'wb').write(blob)
k2=load(o); print([x['ex']==len(k2.plain(x)) for x in k2.rows],len(blob),os.path.getsize(G))
