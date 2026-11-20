"""audit_specific.py - busca casos concretos que el usuario报告: Press Start, Gamillas, AI, etc."""
import sys, os, re
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

G = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data'
C = r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData'
FILES = [
 ('PROLOGUE', G + r'/AIDDATA/EN/Prologue.cpk'),
 ('SYSTEXT',  G + r'/AIDDATA/EN/SysText.cpk'),
 ('STGEST',   G + r'/STAGE/STGEST_EN.CPK'),
 ('CMN00',    G + r'/BTLC/EN0/CMN00.CPK'),
 ('KPACK_LN', G + r'/KURODATA/EN/KPACK_P4_LN_EN.CPK'),
 ('KPACK_RG', G + r'/KURODATA/EN/KPACK_P4_RG_EN.CPK'),
 ('LT00',     C + r'/LanguageData/EN/LT00_EN.cpk'),
 ('B_LT00',   C + r'/LanguageData/EN/B_LT00_EN.cpk'),
 ('MTZKN_NM', C + r'/../MtData/EN/MtZkn_Nm.cpk'),
 ('MTZKN_PT', C + r'/../MtData/EN/MtZkn_Pt.cpk'),
 ('MTZKN_RT', C + r'/../MtData/EN/MtZkn_Rt.cpk'),
]
PATS = [
 ('Press',      re.compile(r'press\s+(any|start|the|a|\+)', re.I)),
 ('Gamillas',   re.compile(r'gamill', re.I)),
 ('AI',         re.compile(r'\bAI\b')),
 ('Soldier',    re.compile(r'\bsoldier(s)?\b', re.I)),
 ('Start',      re.compile(r'\b(start|press start)\b', re.I)),
]

def strings_from(data):
    out=[]
    for part in re.split(rb'[\x00-\x08\x0b\x0c\x0e-\x1f]', data):
        if len(part)<4: continue
        try: s=part.decode('utf-8')
        except Exception: continue
        s=''.join(ch if (ch.isprintable() or ch in '\n\r\t　') else ' ' for ch in s).strip()
        if len(s)>=4: out.append(s)
    return out

for name,p in FILES:
    if not os.path.exists(p): continue
    try: c=load(p)
    except Exception: continue
    pool=[]
    for r in c.rows:
        try:
            pt=c.plain(r); pool+=strings_from(pt)
            if name.startswith('MTZKN'):
                pool+=strings_from(bytes(b^0x5E for b in pt))
        except Exception: pass
    pool=sorted(set(pool))
    hits={k:[] for k,_ in PATS}
    for s in pool:
        for k,pat in PATS:
            if pat.search(s): hits[k].append(s)
    total=sum(len(v) for v in hits.values())
    if total==0: continue
    print('\n##### %s'%name)
    for k,_ in PATS:
        v=hits[k]
        if not v: continue
        print('  -- %s (%d) --'%(k,len(v)))
        for s in v[:8]: print('     '+repr(s[:110]))
    sys.stdout.flush()
