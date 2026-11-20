import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
c = load(r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK')
f4 = [f for f in c.rows if f['id'] == 4][0]
pt = c.plain(f4)
def align4(v): return (v+3)&~3
off = 0x10
n = 0
while off + 0x40 <= len(pt):
    ln = struct.unpack_from('<I', pt, off+0x3c)[0]
    if not (0 < ln <= 0x1000): break
    if n >= 108:
        print('rec %d off=%s ln=%2d key=%r title=%r tail=%s' % (n, hex(off), ln, pt[off:off+4], pt[off+0x40:off+0x40+ln].split(b'\0')[0], pt[off+0x40+ln:off+0x48+align4(ln)].hex(' ')))
    off += 0x48 + align4(ln)
    n += 1
