import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
import kpack_ln as K

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)
rows = {f['id']: f for f in c.rows}
pt = c.plain(rows[4])
count = struct.unpack_from('<I', pt, 0)[0]
print('count', count, 'len', len(pt))

off = 0x10
n = 0
while off + 0x40 <= len(pt):
    key = pt[off:off + 4]
    ln = struct.unpack_from('<I', pt, off + 0x3c)[0]
    if ln == 0 or ln > 0x400:
        print('parada en', hex(off), 'key', key, 'ln', hex(ln), 'resto', len(pt) - off)
        break
    raw = pt[off + 0x40:off + 0x40 + ln]
    nul = raw.find(b'\0')
    txt = raw[:nul] if nul >= 0 else raw
    size = 0x48 + K.align(len(txt) + 1, 4)
    if n < 6 or n > count - 4:
        f = struct.unpack_from('<16I', pt, off + 4)
        print(hex(off), key, 'ln', ln, 'size', size, 'f', [hex(x) for x in f], repr(txt)[:60])
    n += 1
    off += size
print('registros', n, 'off final', hex(off), 'colar', hex(len(pt) - off))
print('resto bytes', pt[off:off + 64].hex(' '))
