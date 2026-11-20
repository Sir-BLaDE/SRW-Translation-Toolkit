import os,sys,hashlib
sys.path.insert(0,'/tmp/b')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
h=os.environ['HOME']; P=h+'/mnt/srwv/'
BASE=P+'backup/SysText_installed_before_names2.cpk'
REP={'Emperor of Darkness':'Emperador Oscuro','Great General of Darkness':'Gran General Oscuro','High-Mobility Unit Black Selena':'Unidad Móvil Black Selena','Aestivalis Custom Hikaru Unit':'Aestivalis Custom de Hikaru','Calidus Multi-phase Beam Cannon':'Cañón multifase Calidus','High Energy Long-range Beam Cannon':'Cañón de rayos largo alcance','Kurogane Five Certain Death Attack':'Ataque Mortal de Kurogane Five'}
c=load(BASE); row=[r for r in c.rows if r['id']==2][0]; pt=bytearray(c.plain(row)); n0=len(pt)
tot=0
for o,nw in REP.items():
    ob=o.encode()+b'\x00'; nb=nw.encode('utf-8')+b'\x00'
    assert len(nb)<=len(ob),(o,len(nb),len(ob))
    i=0;k=0
    while True:
        i=pt.find(ob,i)
        if i<0: break
        pt[i:i+len(ob)]=nb+b'\x00'*(len(ob)-len(nb)); i+=len(ob); k+=1
    print(o,k); tot+=k
newpt=bytes(pt); assert len(newpt)==n0
out=P+'outputs/SysText_es_names3.cpk'
blob=build_ordered(BASE,{2:(c.cipher(row,newpt),len(newpt))}); open(out,'wb').write(blob)
c2=load(out)
for r in c2.rows: assert r['ex']==len(c2.plain(r)),r['id']
assert c2.plain([r for r in c2.rows if r['id']==2][0])==newpt
print('ok',out,len(blob),hashlib.sha256(blob).hexdigest()[:12],tot)
