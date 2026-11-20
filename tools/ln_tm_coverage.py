import sys, io, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
import kpack_ln as kln
from cpk_util import load

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)
tm = json.load(io.open(r'C:/Dev/Default Project/srwv/datos/es_tm.json', encoding='utf-8'))

f0 = [f for f in c.rows if f['id']==0][0]
recs0 = kln.parse0(c.plain(f0))
u0 = sorted({r['text'].decode('utf-8','replace') for r in recs0})

f1 = [f for f in c.rows if f['id']==1][0]
d1 = kln.parse1(c.plain(f1))
u1 = sorted({s.decode('utf-8','replace') for s in d1['strs']})

f3 = [f for f in c.rows if f['id']==3][0]
strs3, _ = kln.parse3(c.plain(f3))
u3 = sorted({s.decode('utf-8','replace') for s in strs3})

f4 = [f for f in c.rows if f['id']==4][0]
count4, recs4 = kln.parse4(c.plain(f4))
u4 = sorted({r['text'].decode('utf-8','replace') for r in recs4})

for name, us in [('id0',u0),('id1',u1),('id3',u3),('id4',u4)]:
    hit = sum(1 for s in us if s in tm)
    print(name, 'unique', len(us), 'TM hit', hit, 'miss', len(us)-hit)
"<rfl:parameter name="