import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
import kpack_ln as K

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)
f4 = [f for f in c.rows if f['id'] == 4][0]
pt = c.plain(f4)
print('total plain len', len(pt))
count = struct.unpack_from('<I', pt, 0)[0]
print('count', count, 'header', pt[:16].hex(' '))

off = 0x10
n = 0
while off + 0x40 <= len(pt):
    key = pt[off:off + 4]
    ln = struct.unpack_from('<I', pt, off + 0x3c)[0]
    if not (0 < ln <= 0x1000):
        print('STOP at', hex(off), 'n', n, 'key', key, 'ln', hex(ln))
        break
    raw = pt[off + 0x40:off + 0x40 + ln]
    txt = raw.split(b'\0')[0]
    size = 0x48 + K.align(ln, 4)
    # use ln directly for stepping (as original format stores full length)
    if n < 5 or off >= 0x2900:
        print(hex(off), key, 'ln', ln, 'size', size, repr(txt)[:70])
    n += 1
    off += size
print('primary records n=', n, 'end off=', hex(off))
print('bytes at end:', pt[off:off + 64].hex(' '))
