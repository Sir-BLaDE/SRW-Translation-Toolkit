import os,sys,csv,pathlib
sys.path.insert(0,'/tmp/b'); sys.path.insert(0,'/tmp/w')
from cpk_util import load
from srwv_cpkbuild2 import build_ordered
from srwv_buildbltu import build
from srwv_bltu import load as lb
from fixpunct import fix
from attacks import apply
h=os.environ['HOME']; P=h+'/mnt/srwv/'
INST=h+'/mnt/Super Robot Wars V/Data/BTLC/EN0/CMN00.CPK'
ORIG=P+'backup/CMN00_CPK_original.cpk'
EX={'Bajada de Movilidad':'Movilidad reducida','Puntería baja':'Puntería reducida','Bajada de Armadura':'Blindaje reducido','Bajada de Vista':'Visión reducida','Bajada de EN':'EN reducida','Subida de Enfoque Máx.':'Enfoque máx. aumentado','Subida de Enfoque':'Enfoque aumentado','Subida de Estado':'Estado mejorado','Subida de Movimiento':'Movimiento aumentado'}
FIXB={'¿Unicorn está impingiendo en\\nla consciencia de Banagher?': '¿Se está apoderando el Unicorn\\nde la conciencia de Banagher?', '¡Banagher! ¡Cierra el Unicorn!': '¡Banagher! ¡Apaga el Unicorn!', '¡Deberías apostar por el\\npotencial de Banagher también!': '¡Deberías confiar también\\nen el potencial de Banagher!', '¡Banagher, mostrar a la gente la posibilidad\\nno los cambiará!': '¡Banagher, enseñarle a la gente la posibilidad\\nno la cambiará!', '¡Te cortaré tu futuro brillante, Banagher Links!': '¡Acabaré con tu brillante futuro, Banagher Links!', '¡El futuro de Banagher Links parece más\\nbrillante por el minuto! ¿Cómo puede ser?': '¡El futuro de Banagher Links brilla más\\na cada minuto! ¿Cómo es posible?', '¡Banagher! ¿Qué tan bajo quieres llevarme?': '¡Banagher! ¿Hasta dónde piensas hacerme llegar?', '¡Maldita sea! ¿Si no puedo derrotar a un Newtype\\nartificial entonces cómo voy a derrotar a Banagher?': '¡Maldita sea! Si no puedo derrotar a un Newtype\\nartificial, ¿cómo voy a derrotar a Banagher?', '¡Esto es Banagher! ¡Atacando!': '¡Aquí Banagher! ¡Atacando!', '¡Esto es Banagher! ¡Te respaldo!': '¡Aquí Banagher! ¡Te respaldo!', '¡Cuidado con tus alrededores, Banagher!': '¡Cuidado con lo que te rodea, Banagher!', '¡Banagher! ¡Te daré un puñetazo de sentido si tengo que!': '¡Banagher! ¡Te meteré algo de sentido a puñetazos si hace falta!', '¿Tienes un deseo de muerte, Banagher?': '¿Tienes ganas de morir, Banagher?', '¡Banagher! ¡Ya es demasiado tarde para nada!': '¡Banagher! ¡Ya es demasiado tarde para todo!'}
ci=load(INST); co=load(ORIG)
ri={r['id']:r for r in ci.rows}; ro={r['id']:r for r in co.rows}
pi=ci.plain(ri[1]); po=co.plain(ro[1])
si=[x[3] for x in lb(pi).all_strings()]; so=[x[3] for x in lb(po).all_strings()]
assert len(si)==len(so)
import re
R3={'Fin Funnels':'Aletas satélite','Los Funnels':'Los cañones satélite','Funnels':'Cañones satélite','Funnel':'Cañón satélite','Full Frontal':'Frontal Total','Tri Bomber':'Triple Bombardero','Battle Bomber':'Bombardero de Combate','Great Mightgaine':'Gran Mightgaine','Lambda Driver':'Motor Lambda'}
P3=re.compile(r'(?<![\wáéíóúñ])('+'|'.join(sorted(map(re.escape,R3),key=len,reverse=True))+r')(?![\wáéíóúñ])')
tr={}; n=0
for a,b in zip(si,so):
    if a==b: continue
    t=FIXB.get(a) or EX.get(a) or fix(apply(P3.sub(lambda m:R3[m.group(1)],a)))
    if t!=a: tr[a]=t
print('cambios',len(tr),'FIXB aplicados',sum(1 for a in tr if a in FIXB))
tmp='/tmp/b/tmp_tr.csv'
with open(tmp,'w',encoding='utf-8',newline='') as f:
    w=csv.writer(f,lineterminator='\n'); w.writerow(['id','en','es'])
    for i,(k,v) in enumerate(tr.items()): w.writerow([i,k,v])
new=build(pi,tmp)
out=P+'outputs/CMN00_CPK_final_es12.cpk'
blob=build_ordered(ORIG,{1:(ci.cipher(ri[1],new),len(new))})
pathlib.Path(out).write_bytes(blob)
c2=load(out)
for r in c2.rows: print(r['id'],r['ex'],len(c2.plain(r)),'OK' if r['ex']==len(c2.plain(r)) else 'FAIL')
s2=[x[3] for x in lb(c2.plain({x['id']:x for x in c2.rows}[1])).all_strings()]
import collections
print(len(s2))
bad=[s for s in s2 if (s.count('?')>s.count('¿')) or (s.count('!')>s.count('¡'))]
print('desbalance tras fix',len(bad)); 
for s in bad[:30]: print(repr(s))
