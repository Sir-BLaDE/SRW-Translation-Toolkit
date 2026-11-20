import sys, io, struct, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from lt00 import load as load_lt

for P in (r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK',
          r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_RG_EN.CPK'):
    print('==', P)
    c = load(P)
    print('  files', len(c.rows), 'align', c.cpk.align, 'diag', c.cpk.diagnose() or 'ok')
    for f in c.rows:
        pt = c.plain(f)
        print('  id', f['id'], f['table'], 'size', f['size'], 'ex', f['ex'],
              'plain', len(pt), 'head', pt[:16].hex(' '))
        if pt[:4] == b'BLTU':
            t = load_lt(pt)
            print('    BLTU magic', pt[:8], 'hdr', [hex(x) for x in t.header])
            print('    count', t.count, 'ids', t.id_count)
            for s in t.strings[:8]:
                print('     ', repr(s)[:90])
