import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
from lt00 import load as load_lt

SRC = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_RG_EN.CPK'
cf = load(SRC)
pt = cf.plain(cf.rows[0])
t = load_lt(pt)
print('blob_end', hex(t.blob_end), 'off_start', hex(t.off_start))
print('zona 0x%x-0x%x:' % (t.blob_end, t.off_start), pt[t.blob_end:t.off_start].hex(' '))
print('ultima cadena termina en', hex(t.blob_end - 1) if pt[t.blob_end-1] == 0 else 'no nul')
# ultimos 64 bytes del blob
print('cola blob', pt[t.blob_end-80:t.blob_end].hex(' '))
