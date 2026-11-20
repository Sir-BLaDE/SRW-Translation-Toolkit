"""audit_untranslated.py - auditoria de texto ingles sin traducir en los CPK instalados."""
import sys, os, re
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

G = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data'
C = r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData'
FILES = [
 ('PROLOGUE',  G + r'/AIDDATA/EN/Prologue.cpk'),
 ('SYSTEXT',   G + r'/AIDDATA/EN/SysText.cpk'),
 ('STGEST',    G + r'/STAGE/STGEST_EN.CPK'),
 ('CMN00',     G + r'/BTLC/EN0/CMN00.CPK'),
 ('KPACK_LN',  G + r'/KURODATA/EN/KPACK_P4_LN_EN.CPK'),
 ('KPACK_RG',  G + r'/KURODATA/EN/KPACK_P4_RG_EN.CPK'),
 ('LT00',      C + r'/LanguageData/EN/LT00_EN.cpk'),
 ('B_LT00',    C + r'/LanguageData/EN/B_LT00_EN.cpk'),
 ('MTZKN_NM',  C + r'/../MtData/EN/MtZkn_Nm.cpk'),
 ('MTZKN_PT',  C + r'/../MtData/EN/MtZkn_Pt.cpk'),
 ('MTZKN_RT',  C + r'/../MtData/EN/MtZkn_Rt.cpk'),
]

# palabras tipicas de texto de juego en ingles
EN_WORDS = re.compile(r'\b(the|you|your|this|that|and|with|for|from|attack|defend|power|level|item|skill|move|range|damage|hit|miss|turn|phase|start|press|select|confirm|cancel|name|point|ability|weapon|pilot|unit|enemy|ally|move|action|end|next|continue|yes|no|ok|are|is|was|will|not|can|do|if|in|on|at|to|of|it|be|or)\b', re.I)

def strings_from(data):
    """Extrae cadenas imprimibles de un blob, dividiendo por nulos y bytes de control."""
    out=[]
    for part in re.split(rb'[\x00-\x08\x0b\x0c\x0e-\x1f]', data):
        if len(part)<4: continue
        try: s=part.decode('utf-8')
        except Exception: continue
        # limpiar
        s=''.join(ch if (ch.isprintable() or ch in '\n\r\t　') else ' ' for ch in s).strip()
        if len(s)<4: continue
        out.append(s)
    return out

for name,p in FILES:
    if not os.path.exists(p):
        print('%-10s NO EXISTE %s'%(name,p)); continue
    try: c=load(p)
    except Exception as e:
        print('%-10s LOAD ERROR %s'%(name,e)); continue
    allstr=[]
    for r in c.rows:
        try: pt=c.plain(r)
        except Exception: continue
        allstr += strings_from(pt)
    # MTZKN viene XOR 0x5E
    if name.startswith('MTZKN'):
        dec=[]
        for r in c.rows:
            try: pt=c.plain(r)
            except Exception: continue
            dec += strings_from(bytes(b^0x5E for b in pt))
        allstr += dec
    uniq=sorted(set(allstr))
    en=[s for s in uniq if EN_WORDS.search(s)]
    print('\n##### %-10s filas=%d cadenas=%d uniq=%d EN-sospechosas=%d'%(
        name,len(c.rows),len(allstr),len(uniq),len(en)))
    for s in en[:12]:
        print('   '+repr(s[:90]))
    sys.stdout.flush()
