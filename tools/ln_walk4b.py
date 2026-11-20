import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
import kpack_ln as K

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)
rows = {f['id']: f for f in c.rows}
pt = c.plain(rows[4])

off = 0x10
n = 0
while off + 0x40 <= len(pt) and n < 200:
    key = pt[off:off + 4]
    ln = struct.unpack_from('<I', pt, off + 0x3c)[0]
    if not (0 < ln <= 0x400) or key[3:4] != b'\x00':
        print('DESYNC en', hex(off), 'n', n, 'key', key, 'ln', hex(ln))
        print('   bytes', pt[off:off + 32].hex(' '))
        print('   anteriores', pt[off - 48:off].hex(' '))
        break
    raw = pt[off + 0x40:off + 0x40 + ln]
    txt = raw.split(b'\0')[0]
    size = 0x48 + K.align(len(txt) + 1, 4)
    if n >= 108:
        print(hex(off), key, 'ln', ln, 'size', size, repr(txt)[:50])
    n += 1
    off += size
