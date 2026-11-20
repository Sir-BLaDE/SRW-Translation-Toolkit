"""audit_full.py - auditoria rapida de los CPK de texto instalados."""
import sys, os, re
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

G = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data'
FILES = [
 ('FONT',      G + r'/AIDDATA/EN/FontInfo.cpk'),
 ('SYSTEXT',   G + r'/AIDDATA/EN/SysText.cpk'),
 ('STGEST',    G + r'/STAGE/STGEST_EN.CPK'),
 ('CMN00',     G + r'/BTLC/EN0/CMN00.CPK'),
 ('KPACK_LN',  G + r'/KURODATA/EN/KPACK_P4_LN_EN.CPK'),
 ('KPACK_RG',  G + r'/KURODATA/EN/KPACK_P4_RG_EN.CPK'),
 ('LT00_EN',  r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/LT00_EN.cpk'),
 ('B_LT00',   r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData/LanguageData/EN/B_LT00_EN.cpk'),
 ('MTZKN_NM', r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/MtZkn_Nm.cpk'),
 ('MTZKN_PT', r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/MtZkn_Pt.cpk'),
 ('MTZKN_RT', r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/MtData/EN/MtZkn_Rt.cpk'),
 ('PROLOGUE', G + r'/AIDDATA/EN/Prologue.cpk'),
]
for root, dirs, files in os.walk(G):
    for f in files:
        if f.upper() in ('LT00.CPK','MTZKN_NM.CPK','MTZKN_PT.CPK','MTZKN_RT.CPK'):
            FILES.append((f.split('.')[0].upper(), os.path.join(root,f)))

seen=set()
print('%-10s %9s %6s %9s %8s %s'%('FILE','SIZE','ROWS','ACCENT','INV','DIAG'))
for name,p in FILES:
    if p in seen or not os.path.exists(p): continue
    seen.add(p)
    try: c=load(p)
    except Exception as e:
        print('%-10s LOAD ERROR %s'%(name,e)); continue
    ok=True
    for r in c.rows:
        try:
            pt=c.plain(r)
            if r['ex']!=len(pt): ok=False
        except Exception: ok=False
    diag=c.cpk.diagnose()
    acc=inv=0
    for r in c.rows:
        try: pt=c.plain(r)
        except Exception: continue
        acc+=pt.count(b'\xc3')+pt.count(b'\xf1')
        inv+=pt.count(b'\xc2\xbf')+pt.count(b'\xc2\xa1')
    print('%-10s %9d %6d %9d %8d %s'%(name,os.path.getsize(p),len(c.rows),acc,inv,('OK' if ok and not diag else 'FAIL %s'%diag)))
    sys.stdout.flush()
