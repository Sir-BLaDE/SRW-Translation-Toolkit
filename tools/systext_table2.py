# -*- coding: utf-8 -*-
import sys,struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/SysText.cpk'
c=load(p)
r=[x for x in c.rows if x['id']==2][0]
pt=c.plain(r)
# tabla2: 128 entradas de 16 bytes desde 0x1640
for i in range(128):
    off=0x1640+i*16
    a,b,cc,d=struct.unpack_from('<IIII',pt,off)
    if i<12 or i in (17,81,127):
        print('%3d 0x%04x  a=%-4d b=%-5d c=0x%x (%d) d=%-5d'%(i,off,a,b,cc,cc,d))
# buscar si b o d coinciden con offsets relativos del banco
offs=[struct.unpack_from('<I',pt,0x1440+i*4)[0] for i in range(128)]
so=set(offs)
match_b=match_d=0
for i in range(128):
    a,b,cc,d=struct.unpack_from('<IIII',pt,0x1640+i*16)
    if b in so: match_b+=1
    if d in so: match_d+=1
print('coincidencias con offsets banco: b=%d d=%d'%(match_b,match_d))
