import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

cf = load(r'C:/Dev/Default Project/srwv/backup/KPACK_P4_LN_EN_original.cpk')
f4 = [f for f in cf.rows if f['id'] == 4][0]
pt = cf.plain(f4)

def align4(v): return (v+3)&~3
off = 0x10
n = 0
full = 0
while off + 0x40 <= len(pt):
    ln = struct.unpack_from('<I', pt, off+0x3c)[0]
    if not (0 < ln <= 0x1000): break
    raw = pt[off+0x40:off+0x40+ln]
    nul = raw.find(b'\0')
    if nul < 0:
        full += 1
        print('NO NULL: rec %d off=%s ln=%d raw=%r' % (n, hex(off), ln, raw))
    off += 0x48 + align4(ln)
    n += 1
print('records', n, 'without null:', full)
