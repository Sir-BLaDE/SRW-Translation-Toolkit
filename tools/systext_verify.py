# -*- coding: utf-8 -*-
import sys,struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p=r'C:/Dev/Default Project/srwv/outputs/SysText_es.cpk'
c=load(p)
r=[x for x in c.rows if x['id']==2][0]
pt=c.plain(r)
BASE=struct.unpack_from('<I',pt,0x18)[0]
size=struct.unpack_from('<I',pt,0x1c)[0]
tab=struct.unpack_from('<I',pt,0x20)[0]
cnt=struct.unpack_from('<I',pt,0x24)[0]
tab2=struct.unpack_from('<I',pt,0x28)[0]
print('len',len(pt),'BASE',BASE,'banco',size,'tabla1',tab,'n',cnt,'tabla2',tab2)
for i in [16,17,18,19,20,21,22,64,81,127]:
    v=struct.unpack_from('<I',pt,tab+i*4)[0]
    s=pt[BASE+v:].split(b'\x00')[0].decode('utf-8','ignore')
    print('%3d off=%-5d %r'%(i,v,s[:100]))
