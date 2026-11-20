import sys, io, re, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)
print('files', len(c.rows), 'diag', c.cpk.diagnose() or 'ok')

for f in c.rows:
    pt = c.plain(f)
    print('== id', f['id'], 'len', len(pt), 'head', pt[:48].hex(' '))
    # cadenas utf-8 imprimibles
    runs = []
    cur = bytearray()
    start = 0
    for i, b in enumerate(pt):
        if 0x20 <= b < 0x7f or b in (0x0a, 0x09):
            if not cur:
                start = i
            cur.append(b)
        else:
            if len(cur) >= 4:
                runs.append((start, bytes(cur)))
            cur = bytearray()
    if len(cur) >= 4:
        runs.append((start, bytes(cur)))
    print('   runs utf8 >=4:', len(runs))
    for off, s in runs[:25]:
        print('    ', hex(off), repr(s.decode('utf-8', 'replace'))[:90])
