import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

p = sys.argv[1] if len(sys.argv)>1 else r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/FontInfo.cpk'
cf = load(p)
rows = {r['id']: r for r in cf.rows}
p0 = cf.plain(rows[0]); p1 = cf.plain(rows[1]); p2 = cf.plain(rows[2]); p3 = cf.plain(rows[3])
print('row0 len',len(p0),'row1 len',len(p1),'row2 len',len(p2),'row3 len',len(p3))
print('row1 head', p1[:64].hex())
print('row0 head', p0[:64].hex())
print('row2 head', p2[:64].hex())
s = p1[48:].decode('utf-8','ignore')
print('map chars', len(s), 'unique', len(set(s)))
for ch in ['a','á','é','í','ó','ú','ñ','¿','¡','?','!','A','Á','É','Í','Ó','Ú','ü','Ü']:
    print(' MAP',repr(ch),'U+%04X'%ord(ch),'in map:', ch in s, 'count', s.count(ch))
# metrics
HDR=40; N=(len(p3)-HDR)//36
byc={}
for g in range(N):
    u=struct.unpack_from('<I',p3,HDR+g*36)[0]
    byc.setdefault(u,g)
for ch in ['á','é','í','ó','ú','ñ','¿','¡','?','!']:
    g=byc.get(ord(ch))
    print(' REC',repr(ch),'U+%04X'%ord(ch),'g=',g)
