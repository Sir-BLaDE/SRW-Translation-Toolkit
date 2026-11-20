import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

# original id4 plain
cf = load(r'C:/Dev/Default Project/srwv/backup/KPACK_P4_LN_EN_original.cpk')
f4 = [f for f in cf.rows if f['id'] == 4][0]
orig = cf.plain(f4)
mod = open(r'C:/Dev/Default Project/srwv/outputs/id4_inplace_on_translated.bin','rb').read()
print('orig len', len(orig), 'mod len', len(mod))

def align4(v): return (v+3)&~3

off = 0x10
n = 0
changed = 0
while off + 0x40 <= len(orig):
    oln = struct.unpack_from('<I', orig, off+0x3c)[0]
    mln = struct.unpack_from('<I', mod, off+0x3c)[0]
    if not (0 < oln <= 0x1000): break
    ot = orig[off+0x40:off+0x40+oln].split(b'\0')[0]
    mt = mod[off+0x40:off+0x40+mln].split(b'\0')[0]
    if ot != mt:
        changed += 1
        print('%3d off=%s oln=%2d mln=%2d %r -> %r' % (n, hex(off), oln, mln, ot.decode('utf-8','replace'), mt.decode('utf-8','replace')))
    off += 0x48 + align4(oln)
    n += 1
print('total changed', changed, 'records', n)
