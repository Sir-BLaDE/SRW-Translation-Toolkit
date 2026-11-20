import sys
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
import kpack_ln as K

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)
rows = {f['id']: f for f in c.rows}
pt3 = c.plain(rows[3])
strs, pos = K.parse3(pt3)
tail = pt3[pos:]
print('id3 cola len', len(tail), 'todo cero', set(tail) == {0})
print('  ', tail[:64].hex(' '))
pt0 = c.plain(rows[0])
recs = K.parse0(pt0)
print('id0 ultimo', hex(recs[-1]['next']), 'texto len', len(recs[-1]['text']))
print('  cola orig', pt0[-24:].hex(' '))
# longitud de la cola del ultimo registro
start = 0
for r in recs[:-1]:
    pass
rb = K.build0(recs)
print('  rb cola', rb[-24:].hex(' '))
print('  rb len', len(rb), 'orig', len(pt0))
