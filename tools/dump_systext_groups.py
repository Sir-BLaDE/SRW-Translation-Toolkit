import sys, io, json, re
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from lt00 import load as load_lt

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/SysText.cpk'
c = load(P)
f = c.rows[0]
t = load_lt(c.plain(f))
groups = []
for a, n, cc in t.ids:
    groups.append((t.strings[a], list(range(cc, cc + n))))
with io.open(r'C:/Dev/Default Project/srwv/datos/systext_groups.txt', 'w', encoding='utf-8', newline='\n') as fh:
    for k, idxs in groups:
        fh.write(f'### {k}  ({len(idxs)})\n')
        for i in idxs:
            fh.write(f'{i}\t{json.dumps(t.strings[i], ensure_ascii=False)}\n')
        fh.write('\n')
print('grupos', len(groups), 'lineas', sum(len(x[1]) for x in groups))
empty = [k for k, idxs in groups if all(not t.strings[i].strip() for i in idxs)]
print('grupos vacios', len(empty))
chars = sum(len(t.strings[i]) for k, idxs in groups for i in idxs)
print('chars totales', chars)
