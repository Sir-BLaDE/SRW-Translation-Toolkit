import sys, io, json, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
import kpack_ln as kln

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)
print('files', len(c.rows), 'diag', c.cpk.diagnose() or 'ok')

for f in c.rows:
    pt = c.plain(f)
    print('\n===== id', f['id'], 'len', len(pt), 'head', pt[:4].hex(' '))
    # try parse0
    try:
        recs = kln.parse0(pt)
        print('  parse0 ->', len(recs), 'recs')
        for r in recs[:5]:
            print('    ', r['key'], repr(r['text'][:60]))
    except Exception as e:
        print('  parse0 err', e)
    # try parse1
    try:
        d = kln.parse1(pt)
        print('  parse1 -> magic', d['magic'], 'count', len(d['strs']))
        for s in d['strs'][:8]:
            print('    ', repr(s[:60]))
    except Exception as e:
        print('  parse1 err', e)
    # try parse3
    try:
        strs, pos = kln.parse3(pt)
        print('  parse3 ->', len(strs), 'strs, consumed', pos, 'of', len(pt))
        for s in strs[:8]:
            print('    ', repr(s[:60]))
    except Exception as e:
        print('  parse3 err', e)
    # try parse4
    try:
        count, recs = kln.parse4(pt)
        print('  parse4 -> count', count, 'recs', len(recs))
        for r in recs[:8]:
            print('    ', r['key'], 'len', r['len'], repr(r['text'][:60]))
    except Exception as e:
        print('  parse4 err', e)