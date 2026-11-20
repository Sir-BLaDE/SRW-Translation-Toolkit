"""verify_es5_installed.py - comprueba mapas y metricas de la fuente es5 instalada."""
import sys,struct
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
W,HDR=4096,40
p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf=load(p); rows={r['id']:r for r in cf.rows}
CHARS=list('áéíóúñÁÉÍÓÚü¿¡')
for rid in (1,2):
    d=cf.plain(rows[rid]); h=[struct.unpack_from('<I',d,i*4)[0] for i in range(12)]
    s=d[h[6]:h[7]].decode('utf-8','ignore')
    print('fila %d: '%rid + ('OK' if all(c in s for c in CHARS) else 'FALTA '+repr([c for c in CHARS if c not in s])))
p3=cf.plain(rows[3]); n=(len(p3)-HDR)//36
byc={}
for g in range(n):
    u=struct.unpack_from('<I',p3,HDR+g*36)[0]; byc.setdefault(u,g)
for ch in CHARS:
    g=byc.get(ord(ch))
    if g is None: print(ch,'SIN GLIFO'); continue
    fl=struct.unpack_from('<8f',p3,HDR+g*36+4)
    print(' %s g=%-4d b=%.0f a=%.0f'%(ch,g,fl[4],fl[5]))
print('filas:',len(cf.rows),'ex==plain:',all(r['ex']==len(cf.plain(r)) for r in cf.rows))
