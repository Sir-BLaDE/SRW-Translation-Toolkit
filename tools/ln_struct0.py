import sys, struct, re
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)
pt = c.plain(c.rows[0])
print('id0 len', len(pt), 'hdr', [hex(x) for x in struct.unpack_from('<4I', pt, 0)])
# buscar claves tipo b'NNN\0' en pitch 0x1a0
for off in range(0, len(pt), 0x1a0):
    if off + 16 > len(pt):
        break
    key = pt[off:off + 4]
    v = struct.unpack_from('<3I', pt, off + 4)
    txt = pt[off + 0x10:off + 0x1a0].split(b'\0')[0]
    print(hex(off), key, [hex(x) for x in v], repr(txt[:60]))
