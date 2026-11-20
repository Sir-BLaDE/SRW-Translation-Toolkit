# -*- coding: utf-8 -*-
import sys,struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/SysText.cpk'
c=load(p)
r=[x for x in c.rows if x['id']==2][0]
pt=c.plain(r)
print('len',len(pt))
for off in range(0,0x120,16):
    ch=pt[off:off+16]
    print('0x%04x %-47s %s'%(off,ch.hex(' '),''.join(chr(x) if 32<=x<127 else '.' for x in ch)))
print('\nu32 en 0x00:')
for i in range(0,0x100,4):
    v=struct.unpack_from('<I',pt,i)[0]
    if v: print(' 0x%03x = %d (0x%x)'%(i,v,v))
