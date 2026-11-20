"""audit_report.py - informe legible: que queda sin traducir y donde."""
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
]
ES_CHARS=set('áéíóúñÁÉÍÓÚ¿¡')
ES_W=re.compile(r'\b(el|la|los|las|un|una|de|del|al|que|es|son|en|y|con|por|para|no|sí|su|sus|este|esta|más|pero|como|cuando|donde|porque|nada|todo|puede|puedes|hay|hasta|desde|entre|sobre|muy|mucho|poco|ahora|aquí|así|bien|me|te|se|nos|les|lo|sido|ser|era|fue|tan|ella|él|nosotros|usted|mi|mis|tu|tus|nuestro|nuestra)\b',re.I)
EN_W=re.compile(r'\b(the|you|your|this|that|these|those|and|with|for|from|attack|defend|defense|power|level|item|skill|move|range|damage|hit|miss|turn|phase|start|press|select|confirm|cancel|name|point|ability|weapon|pilot|unit|enemy|ally|allies|action|end|next|continue|yes|are|was|will|not|can|if|of|it|be|or|but|in|on|at|to|is|have|has|had|do|does|did|what|when|where|who|why|how|out|up|down|left|right|open|close|save|load|data|set|get|use|using|become|increase|decrease|effect|only|also|just|very|more|most|less|than|then|there|here|their|them|his|her|its|our|we|they|he|she|one|two|three|four|five)\b',re.I)
CODE=re.compile(r'(CsCppToCsLua|\.cpp|\.lua|FILE\s*:|@note|require|function|local\s|nil|end\s*$)',re.I)
def sf(data,xor=0):
    out=[]
    if xor: data=bytes(b^xor for b in data)
    for p in re.split(rb'[\x00-\x08\x0b\x0c\x0e-\x1f]',data):
        if len(p)<4: continue
        try:s=p.decode('utf-8')
        except Exception:continue
        s=''.join(c if(c.isprintable() or c in '\n\r\t　') else ' ' for c in s).strip()
        if len(s)>=4:out.append(s)
    return out
def cls(s):
    if CODE.search(s): return 'CODE'
    es=bool(ES_W.search(s)) or any(c in ES_CHARS for c in s)
    en=bool(EN_W.search(s))
    if es and not en:return 'ES'
    if en and not es:return 'EN'
    if es and en:return 'MIXTO'
    return 'NEUTRO'
for name,p in FILES:
    if not os.path.exists(p):continue
    try:c=load(p)
    except Exception:continue
    pool=set()
    for r in c.rows:
        try:
            pt=c.plain(r);pool.update(sf(pt))
            if name.startswith('MTZKN'):pool.update(sf(pt,0x5E))
        except Exception:pass
    cats=collections.Counter(cls(s) for s in pool)
    user_en=[s for s in pool if cls(s)=='EN' and not CODE.search(s)]
    print('\n'+'='*72)
    print('%s  EN-ESTIMADO=%d (de %d uniq; CODE=%d ES=%d MIXTO=%d NEUTRO=%d)'%(
        name,len(user_en),len(pool),cats['CODE'],cats['ES'],cats['MIXTO'],cats['NEUTRO']))
    for s in sorted(user_en)[:30]:
        print('  '+repr(s[:120]))
