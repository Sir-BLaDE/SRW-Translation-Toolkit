import os,sys,re
sys.path.insert(0,'/tmp/b')
from cpk_util import load
D=os.environ['HOME']+'/mnt/Super Robot Wars V/Data/'
files=['AIDDATA/EN/SysText.cpk','KURODATA/EN/KPACK_P4_LN_EN.CPK','KURODATA/EN/KPACK_P4_RG_EN.CPK','AIDDATA/EN/LayoutData.cpk','CommonData/MtData/EN/rpw_jstr.cpk','AIDDATA/EN/Prologue.cpk']
F=['unidad','habilidad','pieza','munición','casilla','mejora','clase','arma','acción','fase','mejoras','piezas','armas','unidades','habilidades']
M=['enfoque','ataque','piloto','robot','nivel','daño','turno','espíritu','comando','objetivo','mapa','equipo','arma\\b']
pat=re.compile(r'\b(un|el|este|ese|del|al|nuevo|otro|ningún)\s+('+'|'.join(F[:8])+r')\b',re.I)
pat2=re.compile(r'\b(una|la|esta|esa|nueva|otra|ninguna)\s+('+'|'.join(M[:-2])+r')\b',re.I)
pat3=re.compile(r'\b(un|una|el|la|los|las)\s*[%{}\$#]|\b[Uu]n\(a\)|\b(un|una)\s+\(')
for f in files:
    p=D+f
    if not os.path.exists(p): print('NO',f);continue
    k=load(p)
    for r in k.rows:
        if r['ex']>20_000_000: continue
        try:b=k.plain(r)
        except Exception: continue
        try:t=b.decode('utf-8','ignore')
        except: continue
        for pt in (pat,pat2,pat3):
            for m in pt.finditer(t):
                s=t[max(0,m.start()-25):m.end()+25].replace('\n','|').replace('\x00','|')
                print(f.split('/')[-1],r['id'],repr(s))
