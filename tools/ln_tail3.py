import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
import kpack_ln as K

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)
rows = {f['id']: f for f in c.rows}
pt = c.plain(rows[3])
strs, pos = K.parse3(pt)
print('pos', hex(pos), 'ultima cadena', repr(strs[-1]))
for base in range(pos - 48, pos + 96, 16):
    print(hex(base), pt[base:base + 16].hex(' '), repr(pt[base:base + 16]))
print('total len', hex(len(pt)))
