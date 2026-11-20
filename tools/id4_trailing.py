import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
import kpack_ln as K

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)
f4 = [f for f in c.rows if f['id'] == 4][0]
pt = c.plain(f4)

def align4(v):
    return (v + 3) & ~3

off = 0x10
for n in range(6):
    ln = struct.unpack_from('<I', pt, off + 0x3c)[0]
    end_title = off + 0x40 + ln
    rec_end = off + 0x48 + align4(ln)
    print('rec %d off=%s ln=%d title=%r' % (n, hex(off), ln, pt[off+0x40:off+0x40+ln]))
    print('   bytes after title to rec_end (%d bytes): %s' % (rec_end-end_title, pt[end_title:rec_end].hex(' ')))
    off = rec_end
