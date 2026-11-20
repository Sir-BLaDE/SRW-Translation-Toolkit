"""backslash_hunt.py - busca barras invertidas sueltas (0x5C) que no formen
un codigo de control valido. En fuentes japonesas 0x5C se pinta como ¥."""
import sys, re, os
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from lt00 import load as load_lt

# codigos de control validos del juego (letras tras la barra)
VALID = set('nrcabcdefghijklmnopqrstuvwxyzN')

def hunt(label, s):
    bad=[]
    for m in re.finditer(r'\\',s):
        nxt=s[m.end():m.end()+1]
        if nxt not in VALID:
            ctx=s[max(0,m.start()-35):m.start()+35].replace('\n',' ').replace('\r',' ')
            bad.append(ctx)
    return bad

# CPK instalados
G=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data'
FILES=[
 ('STGEST', G+r'/STAGE/STGEST_EN.CPK'),
 ('CMN00', G+r'/BTLC/EN0/CMN00.CPK'),
 ('KPACK_LN', G+r'/KURODATA/EN/KPACK_P4_LN_EN.CPK'),
 ('LT00', r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk'),
 ('B_LT00', r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk'),
]
total=0
for name,p in FILES:
    if not os.path.exists(p): continue
    c=load(p)
    for r in c.rows:
        pt=c.plain(r)
        s=pt.decode('utf-8','ignore')
        bad=hunt(name,s)
        if bad:
            total+=len(bad)
            print('=== %s r%d : %d barras sueltas'%(name,r['id'],len(bad)))
            for b in bad[:12]: print('   ',repr(b[:80]))
print('TOTAL barras sueltas:',total)
