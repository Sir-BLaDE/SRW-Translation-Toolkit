import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

for label, path in [('ORIG', r'C:/Dev/Default Project/srwv/backup/KPACK_P4_LN_EN_original.cpk'),
                    ('INST', r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK')]:
    c = load(path)
    f4 = [f for f in c.rows if f['id'] == 4][0]
    pt = c.plain(f4)
    def align4(v): return (v+3)&~3
    off = 0x10
    n = 0
    bad = 0
    while off + 0x40 <= len(pt):
        ln = struct.unpack_from('<I', pt, off+0x3c)[0]
        if not (0 < ln <= 0x1000): break
        tail = pt[off+0x40+ln:off+0x48+align4(ln)]
        if any(tail):
            bad += 1
            print(label, 'rec', n, 'off', hex(off), 'tail nonzero', tail.hex(' '))
        off += 0x48 + align4(ln)
        n += 1
    print(label, 'records', n, 'tail nonzero count', bad)
