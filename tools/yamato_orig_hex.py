"""yamato_orig_hex.py - bytes exactos alrededor de Yamato en el original."""
import sys,re
sys.path.insert(0,r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p=r'C:/Dev/Default Project/srwv/backup/STGEST_EN_original.cpk'
c=load(p)
r=[x for x in c.rows if x['id']==9][0]
pt=c.plain(r)
seen=0
for m in re.finditer(b'Yamato',pt):
    s=pt[max(0,m.start()-6):m.end()+8]
    print(s.hex(' '))
    print('  '+''.join(chr(x) if 32<=x<127 else '.' for x in s))
    seen+=1
    if seen>=8: break
