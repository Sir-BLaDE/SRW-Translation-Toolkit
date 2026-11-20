import sys, io, json, re
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from lt00 import load as load_lt

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/AIDDATA/EN/SysText.cpk'
c = load(P)
t = load_lt(c.plain(c.rows[0]))

def load_map(path):
    dup = []

    def hook(pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                dup.append(k)
            d[k] = v
        return d

    data = json.load(io.open(path, encoding='utf-8'), object_pairs_hook=hook)
    return data, dup

m1, d1 = load_map(r'C:/Dev/Default Project/srwv/datos/systext_es_1.json')
m2, d2 = load_map(r'C:/Dev/Default Project/srwv/datos/systext_es_2.json')
print('parte1', len(m1), 'dups', d1)
print('parte2', len(m2), 'dups', d2)
both = set(m1) & set(m2)
print('claves en ambas partes', len(both))
for k in list(both)[:10]:
    print('  ', repr(k)[:60])

m = {}
m.update(m1)
m.update(m2)

# valores (indices >= 712)
vals = [(i, t.strings[i]) for i in range(712, t.count)]
used = set()
missing = []
for i, s in vals:
    if s in m:
        used.add(s)
        continue
    if s.strip() == '' or s in ('\n', ' ', '　'):
        continue
    if re.match(r'^TK_COMB_REC_LEC_[A-Z_]+$', s):
        continue
    missing.append((i, s))
print('valores totales', len(vals), 'traducidos', len(used), 'sin traducir con texto', len(missing))
for i, s in missing[:40]:
    print('  ', i, repr(s)[:90])

unused = set(m) - used
print('claves sin uso', len(unused))
for k in sorted(unused)[:20]:
    print('  ', repr(k)[:80])

# longitudes
print('--- lineas mas largas de lo permitido ---')
bad = 0
for i, s in vals:
    if s not in m:
        continue
    es = m[s]
    if len(es) > max(len(s) + 6, 76) and '\\n' not in es:
        bad += 1
        print('  ', i, len(s), '->', len(es), repr(s)[:50], '||', repr(es)[:70])
print('total avisos longitud', bad)

# tokens
def toks(s):
    return (len(re.findall(r'\\c[01]', s)), len(re.findall(r'\\a\d\d', s)),
            s.count('\\n'), s.count('%s'), s.count('%d'))
print('--- tokens distintos ---')
for i, s in vals:
    if s not in m:
        continue
    es = m[s]
    if toks(s) != toks(es):
        print('  ', i, toks(s), toks(es), repr(s)[:40], '||', repr(es)[:40])
