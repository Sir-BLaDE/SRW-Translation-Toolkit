# -*- coding: utf-8 -*-
# Fila 4 de KPACK_P4_LN_EN: titulos DLC con campo capacidad (u32 LE justo antes de la cadena). Nueva len < capacidad.
import os,sys,re,struct,hashlib
sys.path.insert(0,'/tmp/b')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
H=os.environ['HOME']; P=H+'/mnt/srwv/'
src=open(P+'tools/ln_audit2.py',encoding='utf8').read()
blk=re.search(r'A\("""(.*?)"""\)',src,re.S).group(1)
D={}
for l in blk.strip().split('\n'):
    k,_,v=l.partition(' => '); D[k]=v.split(' | ')
X={'Galvanizing Hope':['Esperanza viva'],'A Chilling Reunion':['Reencuentro glacial'],'Cosmic Crossroads':['Cruce cósmico'],
'Island Encounter':['Encuentro isleño'],'Thought Patterns':['Patrones mentales'],'A New Hope Grows':['Nueva esperanza'],
'-Earth Federation':['-Federación'],'A Fight Between Men':['Pelea entre hombres'],'A Subtle Difference':['Sutil diferencia'],
'A Disquieting Clash':['Choque inquietante'],'A Grudge Among Men':['Rencor de hombres'],'Bellicose Star Sea':['Mar bélico'],
'Calling Londo Bell':['Llama Londo Bell'],'Calm Seas':['Mar calmo'],'Space Wolf':['Lobo astral'],'Stage Clear':['Superado'],
'An Opened Door':['Puerta abierta'],'Purple Malice':['Malicia morada'],'-Ange\'s Search':['-Busca a Ange'],'A Final Choice':['Elección final'],
"A Life's Vow":['Voto vital'],'Blooming Anew':['Renacer'],'Happy Gift V':['Regalo V Feliz'],'Lovely Gift V':['Regalo V Amor'],
'Contact':['Enlace'],'-Space':['-Cosmos'],'Blood-Splattered Wings':['Alas ensangrentadas'],"Dr. Hell's Final Wager":['Apuesta de Dr. Infierno'],
'A Desperate Battlefield':['Campo desesperado'],"G-Hound's Critical Battle":['Batalla de G-Hound'],'Bonus Scenario Full Pack':['Pack episodios extra'],
'Another Desperate Battlefield':['Otro campo desesperado']}
base=P+'outputs/LN_bis_A01B3.cpk'; orig=P+'backup/KPACK_P4_LN_instalado_antes_audit2.cpk'
c=load(base); r=[x for x in c.rows if x['id']==4][0]; p=bytearray(c.plain(r)); n0=len(p)
o=load(orig); po=o.plain([x for x in o.rows if x['id']==4][0])
done=0; bad=[]
for m in re.finditer(rb'[^\x00]+\x00*',po):
    s,e=m.start(),m.end(); t=po[s:e].rstrip(b'\0')
    try:u=t.decode('utf8')
    except Exception: u=t.decode('latin1')
    key=u if u in D or u in X else None
    if key is None and u.startswith('DL Version'): key='DL Version Purchase Gift Ｖ'
    if key is None: continue
    cap=struct.unpack('<I',po[s-4:s])[0]
    if not (4<=cap<=64): continue
    cands=X.get(key,[])+D.get(key,[])
    ok=None
    for cd in cands:
        nb=cd.encode('utf8')
        if len(nb)<cap: ok=nb;break
    if ok is None: bad.append((s,key,cap));continue
    p[s:s+cap]=ok+b'\x00'*(cap-len(ok)); done+=1
assert len(p)==n0
print('hechas',done,'NOCABE',bad)
blob=build_ordered(base,{4:(c.cipher(r,bytes(p)),len(p))})
out=P+'outputs/KPACK_P4_LN_EN_row4fix.cpk'; open(out,'wb').write(blob)
k=load(out); assert all(q['ex']==len(k.plain(q)) for q in k.rows)
# verificar: bytes fuera de cadenas+capacidad intactos
pn=k.plain([x for x in k.rows if x['id']==4][0]); print(sum(a!=b for a,b in zip(pn,po)),'bytes distintos vs original'); print(hashlib.sha256(blob).hexdigest()[:12])
