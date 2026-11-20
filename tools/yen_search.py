"""yen_search.py - busca simbolos de yen/yen fullwidth y contextos de 'Yamato'
en todos los textos instalados y en los archivos de datos."""
import sys, os, re, json, csv, pathlib
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

YEN = ['¥','￥','\uffe5','\u00a5']
pats = re.compile(r'[¥￥]|Yamato')

# --- buscar en datos -------------------------------------------------------
root = pathlib.Path(r'C:/Dev/Default Project/srwv/datos')
print('=== EN DATOS (/datos) ===')
for p in sorted(root.rglob('*')):
    if not p.is_file() or p.suffix.lower() not in ('.json','.csv','.txt','.jsonl','.md'): continue
    try: s=p.read_text(encoding='utf-8-sig')
    except Exception: continue
    for y in YEN:
        n=s.count(y)
        if n:
            print(' %s: %d x %r' % (p.relative_to(root), n, y))
            for m in list(re.finditer(re.escape(y),s))[:3]:
                print('     ', repr(s[max(0,m.start()-40):m.end()+40].replace('\n',' ')))

# --- buscar en CPK instalados ----------------------------------------------
G = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data'
FILES = [
 ('SYSTEXT',  G + r'/AIDDATA/EN/SysText.cpk'),
 ('STGEST',   G + r'/STAGE/STGEST_EN.CPK'),
 ('CMN00',    G + r'/BTLC/EN0/CMN00.CPK'),
 ('KPACK_LN', G + r'/KURODATA/EN/KPACK_P4_LN_EN.CPK'),
 ('KPACK_RG', G + r'/KURODATA/EN/KPACK_P4_RG_EN.CPK'),
 ('LT00_EN',  r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk'),
 ('B_LT00',   r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk'),
]
print('\n=== EN CPK INSTALADOS ===')
for name,p in FILES:
    if not os.path.exists(p): continue
    c=load(p)
    for r in c.rows:
        pt=c.plain(r)
        try: s=pt.decode('utf-8')
        except UnicodeDecodeError: s=pt.decode('utf-8','ignore')
        s2=s.replace('\u3000',' ')
        for m in pats.finditer(s2):
            ctx=s2[max(0,m.start()-45):m.end()+45].replace('\n',' ').replace('\r',' ')
            print(' %-9s r%d %r : %r' % (name,r['id'],m.group(0),ctx))
