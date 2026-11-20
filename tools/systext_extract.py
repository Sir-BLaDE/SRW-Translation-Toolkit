# -*- coding: utf-8 -*-
"""Extrae todas las cadenas del banco de SysText fila 2 usando la tabla de offsets."""
import sys,struct,json,collections
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/SysText.cpk'
c=load(p)
r=[x for x in c.rows if x['id']==2][0]
pt=c.plain(r)
BASE=0x30
TAB=0x1440
N=128
offs=[struct.unpack_from('<I',pt,TAB+i*4)[0] for i in range(N)]
print('offsets: min',min(offs),'max',max(offs),'第一个',offs[:5],'ultimos',offs[-5:])
# cada offset apunta al inicio de una cadena;el final es el siguiente offset (o 0x1439)
endbank=struct.unpack_from('<I',pt,0x1c)[0]  # 5129
items=[]
for i,o in enumerate(offs):
    if o==0 and i>0: continue
    start=BASE+o
    # siguiente offset mayor
    nxt=[x for x in offs if x>o]
    stop=BASE+(min(nxt) if nxt else endbank)
    raw=pt[start:stop]
    s=raw.split(b'\x00')[0].decode('utf-8','ignore')
    items.append({'i':i,'off':o,'abs':start,'len':len(raw),'s':s})
json.dump(items,open(r'C:/Dev/Default Project/srwv/datos/systext_row2.json','w',encoding='utf-8'),
          ensure_ascii=False,indent=1)
print('items',len(items))
for x in items:
    print('%3d abs=0x%04x len=%-3d %r'%(x['i'],x['abs'],x['len'],x['s'][:100]))
