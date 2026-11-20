import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)
rows = {f['id']: f for f in c.rows}
pt3 = c.plain(rows[3])
print('id3 len', len(pt3))
for base in range(0, 0x140, 0x10):
    chunk = pt3[base:base + 0x10]
    print(hex(base), chunk.hex(' '), repr(chunk))
