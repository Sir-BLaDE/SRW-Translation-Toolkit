# -*- coding: utf-8 -*-
"""Lista cadenas inglesas reales que quedan en la narracion del Prologue instalado."""
import sys, struct, re, json, collections
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/Prologue.cpk'
c=load(p)
# unicamente palabras inglesas que NO son espanolas
EN=re.compile(r'\b(the|you|your|and|with|for|from|attack|battle|power| Federation|Gamillans|humanity|space|Earth|moon|war|crew|fleet|ships|battle|new|year|years|later|will|would|their|they|have|has|been|into|upon|they|before|after|without|through|against|finally|awaits|journey|prepares|meanwhile|remains|leaves|launches|halted|causing|repeat|various|fate|fates|rests|shoulders|final|other|side|hand|gate|remaining|hasten|return|behind|using|planet|readies|itself|first|history|developmen|halted|Jupiter|launches|charting|course|aboard|briefing|maneuvers|tactical|intrepid|heroes|hunker|Japan|opportunity|counterattack|element|conspires|capitalize|tense|times|chaos|rescued|clutches|Holy|Empire|carries|toward|brief|needed|rest|successfully|executed|plan|Eighth|Angel|vanquished|opportunity|celebrate|though|soon|see|now|such|festivities|outnumbered|heavily|HQ|orders|space|tables|control|Laser|definitive|end|galactic|waged|entrusted|pow|cooperative|organization|formed|reunited|enjoy|respite|fray|say|final|goodbyes|friends|loved|ones|prepare|depart|attempt|stop|fusion|call|managing|factories|absence|ominous|shadow|creeps|closer|precious|enterprise|captains|each|ship|listen|intently|departure|passing|Balun|reaches|Large|Magellanic|Cloud|other|side|where|they|pause|survey|landscape|draw|new|plans|multiple|paths|stretch|sea|stars|before|overcome|deeply|unsettling|feeling|tensions|running|high|throughout|fleet|decisive|looming|series|squabbles|might|erupt|any|moment|makes|preparations|uncertainty|once|again)\b', re.I)
seen=collections.OrderedDict()
for r in c.rows:
    if r['id']==7: continue
    pt=c.plain(r); cnt=struct.unpack_from('<H',pt,0)[0]
    if not cnt or len(pt)<24 or (len(pt)-24)%cnt: continue
    slot=(len(pt)-24)//cnt; meta=slot-22
    for si in range(cnt):
        b=pt[24+si*slot:24+(si+1)*slot]
        for s in b[:meta].split(b'\x00'):
            t=s.decode('utf-8','ignore').strip()
            if len(t)<8: continue
            if any(ch in t for ch in 'áéíóúñ¿¡'): continue  # ya espanol
            if EN.search(t): seen[t]=None
print('cadenas inglesas reales restantes:',len(seen))
for t in seen: print(' ',repr(t))
