import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from lt00 import load as load_lt

SRC = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_RG_EN.CPK'
cf = load(SRC)
pt = cf.plain(cf.rows[0])
t = load_lt(pt)
rb = t.build(list(t.strings))
print('orig', len(pt), 'rebuilt', len(rb))
n = min(len(pt), len(rb))
diffs = [i for i in range(n) if pt[i] != rb[i]]
print('bytes distintos', len(diffs), 'primero', hex(diffs[0]) if diffs else None)
# agrupar
if diffs:
    runs = []
    s = diffs[0]
    p = s
    for i in diffs[1:]:
        if i == p + 1:
            p = i
            continue
        runs.append((s, p))
        s = p = i
    runs.append((s, p))
    print('tramos', len(runs))
    for a, b in runs[:20]:
        print('  ', hex(a), '-', hex(b), b - a + 1, 'orig', pt[a:b+1][:24].hex(), 'new', rb[a:b+1][:24].hex())
    # contexto de las entradas
    print('id_start', hex(t.id_start), 'count', t.id_count)
    for k in range(min(3, t.id_count)):
        off = t.id_start + k * 32
        print('entry', k, 'orig', pt[off:off+32].hex())
        print('       new ', rb[off:off+32].hex())
