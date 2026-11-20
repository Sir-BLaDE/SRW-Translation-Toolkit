# -*- coding: utf-8 -*-
import sys,struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/SysText.cpk'
c=load(p)
r=[x for x in c.rows if x['id']==2][0]
pt=c.plain(r)
targets=[0x1d1,0xbb6,0x1e8,0x23e]
print('len',len(pt),'hex',hex(len(pt)))
for t in targets:
    rel=t-0x30
    hits=[]
    for i in range(0,len(pt)-3,4):
        v=struct.unpack_from('<I',pt,i)[0]
        if v==rel: hits.append(i)
    print('cadena 0x%04x rel=%d(0x%x) referencias en:'%(t,rel,rel),[hex(h) for h in hits])
# ver que hay despues de 0x1680
print('\n--- desde 0x1680 ---')
for off in range(0x1680,min(len(pt),0x1780),16):
    ch=pt[off:off+16]
    print('0x%04x %-47s %s'%(off,ch.hex(' '),''.join(chr(x) if 32<=x<127 else '.' for x in ch)))
# ultimos bytes
print('\n--- ultimos 64 bytes ---')
ch=pt[-64:]
print(ch.hex(' '))
