# -*- coding: utf-8 -*-
"""Verifica el contenido espanol del Prologue instalado."""
import sys, struct, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/Prologue.cpk'
c = load(p)
META=22
print('=== cadenas espanolas en el Prologue instalado ===')
count=0
for r in c.rows:
    pt=c.plain(r); cnt=struct.unpack_from('<H',pt,0)[0]
    if not cnt or len(pt)<24 or (len(pt)-24)%cnt: continue
    slot=(len(pt)-24)//cnt; meta=slot-META
    if r['id']==7: continue  # creditos
    for si in range(cnt):
        b=pt[24+si*slot:24+(si+1)*slot]
        for s in b[:meta].split(b'\x00'):
            if not s: continue
            t=s.decode('utf-8','ignore')
            if any(ch in t for ch in 'áéíóúñ¿¡') and len(t)>5:
                print(' r%-3s s%-3d %s'%(r['id'],si,t))
                count+=1
                if count>=40: break
        if count>=40: break
    if count>=40: break
print('\ntotal mostradas:',count)
# buscar texto ingles residual en narracion
import re
EN=re.compile(r'\b(the|you|and|with|for|from|attack|power|battle| Federation|Gamillans|humanity|space|Earth|moon|war|era)\b')
res=[]
for r in c.rows:
    if r['id']==7: continue
    pt=c.plain(r); cnt=struct.unpack_from('<H',pt,0)[0]
    if not cnt or len(pt)<24 or (len(pt)-24)%cnt: continue
    slot=(len(pt)-24)//cnt; meta=slot-META
    for si in range(cnt):
        b=pt[24+si*slot:24+(si+1)*slot]
        for s in b[:meta].split(b'\x00'):
            t=s.decode('utf-8','ignore').strip()
            if len(t)>15 and EN.search(t): res.append(t)
print('texto ingles residual en narracion:',len(res))
for t in res[:15]: print('  ',repr(t[:90]))
