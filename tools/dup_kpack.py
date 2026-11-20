import sys, io, json, collections
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from lt00 import load as load_lt

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_RG_EN.CPK'
c = load(P)
t = load_lt(c.plain(c.rows[0]))

# mapa indice -> grupo
grp = {}
for a, n, cc in t.ids:
    for i in range(cc, cc + n):
        grp[i] = t.strings[a]

bytext = collections.defaultdict(list)
key_idx = {a for a, b, cc in t.ids}
for i in range(t.count):
    if i in key_idx:
        continue
    bytext[t.strings[i]].append(i)

for s, idxs in bytext.items():
    if len(idxs) > 1 and s.strip():
        print('DUP', idxs, repr(s)[:80])
        for i in idxs:
            print('    ', i, 'grupo', grp.get(i))
