import sys, io, json, struct, collections
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
import kpack_ln as kln

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)

# id0
f0 = [f for f in c.rows if f['id']==0][0]
pt0 = c.plain(f0)
recs0 = kln.parse0(pt0)
print('id0 recs', len(recs0))
# id1
f1 = [f for f in c.rows if f['id']==1][0]
pt1 = c.plain(f1)
d1 = kln.parse1(pt1)
print('id1 strs', len(d1['strs']))
# id3
f3 = [f for f in c.rows if f['id']==3][0]
pt3 = c.plain(f3)
strs3, _ = kln.parse3(pt3)
print('id3 strs', len(strs3))
# id4
f4 = [f for f in c.rows if f['id']==4][0]
pt4 = c.plain(f4)
count4, recs4 = kln.parse4(pt4)
print('id4 recs', len(recs4))

# unique sets
u0 = sorted({r['text'].decode('utf-8','replace') for r in recs0})
u1 = sorted({s.decode('utf-8','replace') for s in d1['strs']})
u3 = sorted({s.decode('utf-8','replace') for s in strs3})
u4 = sorted({r['text'].decode('utf-8','replace') for r in recs4})
print('unique id0', len(u0), 'id1', len(u1), 'id3', len(u3), 'id4', len(u4))

# dump to files
io.open(r'C:/Dev/Default Project/srwv/datos/ln_id0.txt','w',encoding='utf-8').write('\n'.join(u0))
io.open(r'C:/Dev/Default Project/srwv/datos/ln_id1.txt','w',encoding='utf-8').write('\n'.join(u1))
io.open(r'C:/Dev/Default Project/srwv/datos/ln_id3.txt','w',encoding='utf-8').write('\n'.join(u3))
io.open(r'C:/Dev/Default Project/srwv/datos/ln_id4.txt','w',encoding='utf-8').write('\n'.join(u4))
print('dumped')