import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)
pt = c.plain(c.rows[0])
off = 0
n = 0
while off + 16 <= len(pt):
    key = pt[off:off + 4]
    a, nxt, d = struct.unpack_from('<3I', pt, off + 4)
    end = nxt if nxt else len(pt)
    txt = pt[off + 16:end]
    nul = txt.find(b'\0')
    if nul >= 0:
        txt = txt[:nul]
    print(hex(off), key, 'next', hex(nxt), 'cap', end - off - 16, 'len', len(txt))
    print('   ', repr(txt.decode('utf-8', 'replace'))[:160])
    n += 1
    if nxt <= off or nxt > len(pt):
        print('   FIN, siguiente invalido')
        break
    off = nxt
print('registros', n, 'off final', hex(off), 'len', hex(len(pt)))
