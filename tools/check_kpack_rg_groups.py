import sys, io, json, re, collections
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from lt00 import load as load_lt

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/1_KPACK_P4_RG_EN.CPK'
c = load(P)
t = load_lt(c.plain(c.rows[0]))
trans = json.load(io.open(r'C:/Dev/Default Project/srwv/datos/kpack_rg_es.json', encoding='utf-8'))
OVERRIDES = {501: 'El Programa de Habilidad usado en [PILOT]'}

def toks(s):
    return (re.findall(r'\\c[01]', s) + re.findall(r'\\a\d\d', s) +
            ['\\n']*s.count('\\n') + ['%s']*s.count('%s') + ['%d']*s.count('%d') +
            re.findall(r'\[[A-Z_0-9]+\]', s) + ['【']*s.count('【') + ['「']*s.count('「'))

# group-level check
bad_groups = 0
for a, n, cc in t.ids:
    en_toks = []
    es_toks = []
    for i in range(cc, cc+n):
        en_toks += toks(t.strings[i])
        s = t.strings[i]
        es = OVERRIDES.get(i, trans.get(s, s))
        es_toks += toks(es)
    if collections.Counter(en_toks) != collections.Counter(es_toks):
        bad_groups += 1
        print('GROUP TOKEN MISMATCH key=', repr(t.strings[a])[:60])
        print('  en', collections.Counter(en_toks))
        print('  es', collections.Counter(es_toks))
print('grupos con mismatch de tokens:', bad_groups, 'de', len(t.ids))