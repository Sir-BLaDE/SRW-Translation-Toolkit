"""yamato_hex.py - volca los bytes alrededor de 'Yamato' en la historia instalada."""
import sys, re
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
p=r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/STAGE/STGEST_EN.CPK'
c=load(p)
for r in c.rows:
    pt=c.plain(r)
    for m in re.finditer(b'Yamato',pt):
        s=pt[max(0,m.start()-15):m.end()+30]
        print('r%-3d @%-8d %s' % (r['id'],m.start(),s.hex(' ')))
        print('        ascii:', ''.join(chr(x) if 32<=x<127 else '.' for x in s))
