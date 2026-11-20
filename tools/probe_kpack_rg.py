import sys, struct
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from lt00 import load as load_lt

SRC = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_RG_EN.CPK'
cf = load(SRC)
pt = cf.plain(cf.rows[0])
t = load_lt(pt)
print('len', len(pt))
print('hdr', [hex(x) for x in t.header])
# buscar la tabla de offsets: 530 u32 crecientes empezando en 0
n = t.count
for cand in range(0x4000, 0x4400):
    vals = struct.unpack_from('<%dI' % n, pt, cand)
    if vals[0] == 0 and all(vals[i] < vals[i+1] for i in range(n-1)) and vals[-1] < 0x4106:
        print('tabla offsets en', hex(cand), 'ultimo', hex(vals[-1]))
# comprobar header[8]
print('u32 en hdr[8]', hex(struct.unpack_from('<I', pt, t.off_start)[0]))
print('u32 en hdr[8]+4', hex(struct.unpack_from('<I', pt, t.off_start + 4)[0]))
print('ultimo offset en hdr[8]', hex(struct.unpack_from('<I', pt, t.off_start + 4 * (n - 1))[0]))
print('blob end', hex(t.blob_end), 'off_start', hex(t.off_start), 'gap', t.off_start - t.blob_end)
print('id_start', hex(t.id_start), 'fin esperado', hex(t.id_start + 32 * t.id_count), 'len', hex(len(pt)))
