import sys, io, json, re
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from lt00 import load as load_lt

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_RG_EN.CPK'
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

m, dups = load_map(r'C:/Dev/Default Project/srwv/datos/kpack_rg_es.json')
print('claves', len(m), 'dups', dups)

key_idx = {a for a, b, cc in t.ids}
vals = [(i, t.strings[i]) for i in range(t.count) if i not in key_idx]
print('valores', len(vals))

used = set()
missing = []
for i, s in vals:
    if s in m:
        used.add(s)
        continue
    missing.append((i, s))
print('traducidos', len(used), 'sin traducir', len(missing))
for i, s in missing:
    print('  MISS', i, repr(s)[:100])

unused = set(m) - used
print('claves sin uso', len(unused))
for k in sorted(unused):
    print('  UNUSED', repr(k)[:100])

def toks(s):
    return (re.findall(r'\\\\c[01]', s), re.findall(r'\\\\a\d\d', s),
            s.count('\\\\n'), s.count('%s'), s.count('%d'),
            re.findall(r'\[[A-Z_0-9]+\]', s), s.count('【'), s.count('「'))

print('--- tokens distintos ---')
bad_tok = 0
for i, s in vals:
    if s not in m:
        continue
    es = m[s]
    a, b = toks(s), toks(es)
    if a != b:
        bad_tok += 1
        print('  TOK', i, a, '||', b, repr(s)[:50], '->', repr(es)[:50])
print('total avisos tokens', bad_tok)

print('--- longitudes ---')
bad_len = 0
for i, s in vals:
    if s not in m:
        continue
    es = m[s]
    if len(es) > max(len(s) + 6, 76):
        bad_len += 1
        print('  LEN', i, len(s), '->', len(es), repr(s)[:50], '||', repr(es)[:70])
print('total avisos longitud', bad_len)

print('--- vacios o sin acentos sospechosos ---')
for i, s in vals:
    if s not in m:
        continue
    es = m[s]
    if s.strip() and not es.strip():
        print('  EMPTY', i, repr(s)[:60])
