"""audit_comprehensive.py - auditoria exhaustiva de texto sin traducir.

Clasifica TODAS las cadenas de cada CPK instalado en:
  ES    : marcadores de espanol claros
  EN    : marcadores de ingles claros y NINGuno de espanol -> sin traducir
  MIXTO : ambos -> traduccion parcial
  NEUTRO: sin marcadores (nombres, numeros, codigos)
Guarda el detalle en datos/audit_untranslated.txt y un resumen por categoria.
"""
import sys, os, re, collections
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

G  = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data'
CS = r'D:/Juegos/-SPARROW-/Super Robot Wars V/CommonData/ShiroData'
FILES = [
 ('PROLOGUE', G + r'/AIDDATA/EN/Prologue.cpk'),
 ('SYSTEXT',  G + r'/AIDDATA/EN/SysText.cpk'),
 ('STGEST',   G + r'/STAGE/STGEST_EN.CPK'),
 ('CMN00',    G + r'/BTLC/EN0/CMN00.CPK'),
 ('KPACK_LN', G + r'/KURODATA/EN/KPACK_P4_LN_EN.CPK'),
 ('KPACK_RG', G + r'/KURODATA/EN/KPACK_P4_RG_EN.CPK'),
 ('LT00',     CS + r'/LanguageData/EN/LT00_EN.cpk'),
 ('B_LT00',   CS + r'/LanguageData/EN/B_LT00_EN.cpk'),
 ('MTZKN_NM', CS + r'/../MtData/EN/MtZkn_Nm.cpk'),
 ('MTZKN_PT', CS + r'/../MtData/EN/MtZkn_Pt.cpk'),
 ('MTZKN_RT', CS + r'/../MtData/EN/MtZkn_Rt.cpk'),
 ('RPW_JSTR', CS + r'/../MtData/EN/rpw_jstr.cpk'),
]
# DLC descargables (30 CPK)
for _n in sorted(os.listdir(G + r'/DLCDIRE/EN')):
    if _n.lower().startswith('dlc') and _n.lower().endswith('.cpk'):
        FILES.append(('DLC_' + _n[4:7].upper(), G + r'/DLCDIRE/EN/' + _n))

ES_CHARS = set('áéíóúñÁÉÍÓÚ¿¡')
# palabras espanolas inequivocas (baja colision con ingles)
ES_WORDS = re.compile(r'\b(el|la|los|las|un|una|unos|unas|de|del|al|que|es|son|en|y|con|por|para|no|sí|si|su|sus|este|esta|estos|estas|más|pero|como|cuando|donde|porque|nada|todo|todos|tambien|también|puede|puedes|hay|hasta|desde|entre|sobre|bajo|ante|tras|muy|mucho|poco|ahora|aqui|aquí|asi|así|bien|mal|me|te|se|nos|os|les|lo|le|du|da|do|la|sido|ser|era|fue|tan|tanto|ella|él|ello|nosotros|usted|ustedes|mi|mis|tu|tus|nuestro|nuestra|vue|vuestro)\b', re.I)
EN_WORDS = re.compile(r'\b(the|you|your|yours|this|that|these|those|and|with|for|from|attack|defend|defense|power|level|item|skill|move|range|damage|hit|miss|turn|phase|start|press|select|confirm|cancel|name|point|ability|weapon|pilot|unit|enemy|ally|allies|action|end|next|continue|yes|are|was|will|not|can|if|of|it|be|or|but|in|on|at|to|is|have|has|had|do|does|did|what|when|where|who|why|how|now|not|out|up|down|left|right|open|close|save|load|data|set|get|use|using|become|becomes|increase|decrease|effect|effective|only|also|just|very|more|most|less|than|then|there|here|their|them|his|her|its|our|my|me|we|they|he|she|one|two|three|four|five)\b', re.I)

def strings_from(data, xor=0):
    out=[]
    if xor: data=bytes(b^xor for b in data)
    for part in re.split(rb'[\x00-\x08\x0b\x0c\x0e-\x1f]', data):
        if len(part)<4: continue
        try: s=part.decode('utf-8')
        except Exception: continue
        s=''.join(ch if (ch.isprintable() or ch in '\n\r\t　') else ' ' for ch in s).strip()
        if len(s)>=4: out.append(s)
    return out

def classify(s):
    es=bool(ES_WORDS.search(s)) or any(c in ES_CHARS for c in s)
    en=bool(EN_WORDS.search(s))
    if es and not en: return 'ES'
    if en and not es: return 'EN'
    if es and en: return 'MIXTO'
    return 'NEUTRO'

report=[]
summary=collections.OrderedDict()
for name,p in FILES:
    if not os.path.exists(p): continue
    try: c=load(p)
    except Exception as e:
        report.append('%s: LOAD ERROR %s'%(name,e)); continue
    pool=set()
    for r in c.rows:
        try: pt=c.plain(r)
        except Exception: continue
        pool.update(strings_from(pt))
        if name.startswith('MTZKN'):
            pool.update(strings_from(pt,0x5E))
    cats=collections.Counter(classify(s) for s in pool)
    summary[name]=cats
    report.append('\n'+'='*70)
    report.append('%s  (%s)  total uniq=%d  EN=%d MIXTO=%d ES=%d NEUTRO=%d'%(
        name,os.path.basename(p),len(pool),cats['EN'],cats['MIXTO'],cats['ES'],cats['NEUTRO']))
    for cat in ('EN','MIXTO'):
        items=sorted(s for s in pool if classify(s)==cat)
        if not items: continue
        report.append('  --- %s (%d), primeros 40 ---'%(cat,len(items)))
        for s in items[:40]:
            report.append('    '+repr(s[:110]))

out=r'C:/Dev/Default Project/srwv/datos/audit_untranslated.txt'
open(out,'w',encoding='utf-8').write('\n'.join(report))
print('RESUMEN')
print('%-10s %8s %8s %8s %8s %8s'%('CPK','UNIQ','EN','MIXTO','ES','NEUTRO'))
for name,cats in summary.items():
    tot=sum(cats.values())
    print('%-10s %8d %8d %8d %8d %8d'%(name,tot,cats['EN'],cats['MIXTO'],cats['ES'],cats['NEUTRO']))
print('\ndetalle ->',out)
