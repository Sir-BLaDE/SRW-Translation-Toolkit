# -*- coding: utf-8 -*-
import sys,struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/SysText.cpk'
c=load(p)
r=[x for x in c.rows if x['id']==2][0]
pt=c.plain(r)
# buscar valores de offsets de las cadenas que queremos cambiar, en la zona de tablas 0x1440..fin
targets={17:417, 81:2950, 16:398, 80:2915, 22:526, 86:3059}
for idx,val in targets.items():
    hits=[]
    for i in range(0x1440,len(pt)-3,4):
        if struct.unpack_from('<I',pt,i)[0]==val: hits.append(hex(i))
    print('cadena %d offset %d -> refs %s'%(idx,val,hits))
# entender segunda tabla: buscar patron de 16 bytes
print('\nraw 0x1640..0x1680:',pt[0x1640:0x1680].hex(' '))
print('raw 0x1e00..fin:',pt[0x1e00:].hex(' '))
