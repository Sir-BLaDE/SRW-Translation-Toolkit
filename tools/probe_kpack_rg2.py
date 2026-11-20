import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from lt00 import load as load_lt

SRC = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_RG_EN.CPK'
cf = load(SRC)
t = load_lt(cf.plain(cf.rows[0]))
rb = t.build(list(t.strings))
print('len rb', len(rb), 'hdr', [hex(x) for x in struct.unpack_from('<12I', rb, 0)])
t2 = load_lt(rb)
print('reload count', t2.count, 'ids', t2.id_count, 'strings eq', t2.strings == t.strings, 'ids eq', t2.ids == t.ids)
print('off_start', hex(t2.off_start), 'id_start', hex(t2.id_start))
print('tail hex', rb[-32:].hex())
