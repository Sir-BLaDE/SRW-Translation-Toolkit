"""cmn_cleanup.py - limpieza sistematica del CSV de batalla:
  * quita '¡' redundante tras coma/punto y coma
  * reinserta '\\n' cuando el original lo tenia y la traduccion lo perdio
  * parte lineas muy largas para que no se salgan del cuadro
"""
import sys, csv, re, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

SRC = r'C:/Dev/Default Project/srwv/datos/lineas_batalla.csv'
OUT = r'C:/Dev/Default Project/srwv/datos/lineas_batalla_final.csv'
NL = '\\n'   # dos caracteres: barra invertida + n

# correcciones manuales de traducciones claramente erróneas
FIX = {
 '1083': '¡Protege a nuestro aliado inmovilizado! ¡Toda la tripulación, prepárate para el impacto!',
 '1134': '¡Todas las unidades, mantente al día!',
 '2176': '¡Millón α1!',
 '5777': '¡Me han dado!',
 '5765': '¡No tenemos margen para reparaciones!\\n¡No puedo dejarme golpear tan fácilmente!',
 '10488': '|¡Vamos! ¡Vamos, vamos!',
 '23931': '¡Seguridad desactivada!',
 '7875': '¡No hay que entrar en pánico!',
}

cf = load(r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk')
rows = {r['id']: r for r in cf.rows}; p3 = cf.plain(rows[3]); HDR=40; W=4096; N=(len(p3)-HDR)//36
adv={}
for g in range(N):
    off=HDR+g*36; u=struct.unpack_from('<I',p3,off)[0]; fl=struct.unpack_from('<8f',p3,off+4)
    adv.setdefault(u,fl[5])
def width(s):
    s=re.sub(r'\\c\d|\\a\d\d|\$[A-Za-z]\w*|%[ds]','',s)
    parts=re.split(r'\\n',s)
    return max(sum(adv.get(ord(c),20.0) for c in p) for p in parts)
def clean_punct(s):
    s=s.replace(', ¡',', ').replace('; ¡','; ').replace('! ¡','! ¡')
    s=s.replace('¡¡','¡').replace('¿¿','¿')
    s=s.replace(', ¿',', ')
    return s
def split_balanced(s):
    """Devuelve (a,b) partiendo por signo de puntuación cerca del medio."""
    cands=[]
    for i,ch in enumerate(s):
        if ch in ',;:!?' and 0 < i < len(s)-1:
            a=s[:i+1].rstrip(); b=s[i+1:].lstrip()
            if a and b: cands.append((abs(width(a)-width(b)),a,b))
    if not cands:
        # por palabra
        words=s.split(' '); best=None
        for i in range(1,len(words)):
            a=' '.join(words[:i]); b=' '.join(words[i:])
            d=abs(width(a)-width(b))
            if best is None or d<best[0]: best=(d,a,b)
        return (best[1],best[2]) if best else (s,'')
    cands.sort(key=lambda x:x[0])
    return cands[0][1], cands[0][2]

rowsout=[]; stats={'punct':0,'lostnl':0,'split':0}
for r in csv.DictReader(open(SRC,encoding='utf-8-sig',newline='')):
    en,es=r['en'],r['es']
    if es:
        orig=es
        es=clean_punct(es)
        if es!=orig: stats['punct']+=1
        if r['id'] in FIX: es=FIX[r['id']]
        w_en=width(en); w_es=width(es)
        if NL in en and NL not in es:
            a,b=split_balanced(es)
            if b:
                es=a+NL+b; stats['lostnl']+=1
        elif NL not in es and w_es>max(w_en*1.12, 1000):
            a,b=split_balanced(es)
            if b and width(a)<w_es*0.8:
                es=a+NL+b; stats['split']+=1
    rowsout.append((r['id'],en,es))

with open(OUT,'w',encoding='utf-8',newline='') as f:
    w=csv.writer(f); w.writerow(['id','en','es']); w.writerows(rowsout)
print('escrito',OUT,'filas',len(rowsout),'stats',stats)
