import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)
f4 = [f for f in c.rows if f['id'] == 4][0]
pt = c.plain(f4)

base = 0x2bb0
print('len', len(pt), 'from', hex(base), 'remaining', len(pt) - base)
for i in range(base, min(base + 0x200, len(pt)), 16):
    chunk = pt[i:i+16]
    print(hex(i), chunk.hex(' '), repr(chunk))
