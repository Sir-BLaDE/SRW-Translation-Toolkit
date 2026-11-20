"""prologue_row3_hex.py - estructura binaria de la fila 3 del Prologue (EN)."""
import sys
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/Prologue.cpk'
c=load(p)
r=[x for x in c.rows if x['id']==3][0]
pt=c.plain(r)
print('len',len(pt))
for off in range(0,min(len(pt),400),16):
    chunk=pt[off:off+16]
    print('%04x  %-47s %s'%(off,chunk.hex(' '),''.join(chr(x) if 32<=x<127 else '.' for x in chunk)))
print('--- Yamato contexts hex ---')
import re
for m in re.finditer(b'Yamato',pt):
    s=pt[max(0,m.start()-24):m.end()+24]
    print('@%d'%m.start(),s.hex(' '))
    print('       ',''.join(chr(x) if 32<=x<127 else '.' for x in s))
