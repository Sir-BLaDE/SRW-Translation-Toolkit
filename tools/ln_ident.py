import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
import kpack_ln as K

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)
rows = {f['id']: f for f in c.rows}

for fid in (0, 1, 3):
    pt = c.plain(rows[fid])
    if fid == 0:
        recs = K.parse0(pt)
        rb = K.build0(recs)
        print('id0 recs', len(recs), 'len', len(pt), 'rb', len(rb), 'identico', rb == pt)
        if rb != pt:
            d = [i for i in range(min(len(pt), len(rb))) if pt[i] != rb[i]]
            print('   primer diff', hex(d[0]) if d else None, 'n', len(d))
            if d:
                i = d[0]
                print('   orig', pt[i - 8:i + 24].hex(' '))
                print('   new ', rb[i - 8:i + 24].hex(' '))
    elif fid == 1:
        d = K.parse1(pt)
        rb = K.build1(d)
        print('id1 count', len(d['strs']), 'len', len(pt), 'rb', len(rb), 'identico', rb == pt)
        if rb != pt:
            diff = [i for i in range(min(len(pt), len(rb))) if pt[i] != rb[i]]
            print('   primer diff', hex(diff[0]) if diff else None, 'n', len(diff))
            i = diff[0]
            print('   orig', pt[max(0, i - 8):i + 24].hex(' '))
            print('   new ', rb[max(0, i - 8):i + 24].hex(' '))
    else:
        strs, pos = K.parse3(pt)
        rb = K.build3(strs)
        print('id3 strs', len(strs), 'pos', hex(pos), 'len', len(pt), 'rb', len(rb), 'identico', rb == pt)
        if rb != pt:
            diff = [i for i in range(min(len(pt), len(rb))) if pt[i] != rb[i]]
            print('   primer diff', hex(diff[0]) if diff else None, 'n', len(diff))
            i = diff[0]
            print('   orig', pt[max(0, i - 12):i + 24].hex(' '))
            print('   new ', rb[max(0, i - 12):i + 24].hex(' '))
