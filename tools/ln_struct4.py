import sys, struct, re
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)
rows = {f['id']: f for f in c.rows}
pt = c.plain(rows[4])
print('id4 len', len(pt), 'count', struct.unpack_from('<I', pt, 0)[0])

keys = []
for m in re.finditer(rb'[0-9]{3}[A-Za-z]\x00', pt):
    keys.append(m.start())
print('claves', len(keys), 'primeras', [hex(k) for k in keys[:10]])
print('deltas', [keys[i+1]-keys[i] for i in range(min(len(keys)-1, 25))])
print('ultima', hex(keys[-1]), 'fin', hex(len(pt)), 'delta final', len(pt) - keys[-1])

# volcar campos de los 3 primeros registros
for base in keys[:3]:
    end = base + 0x60
    print('== reg', hex(base), repr(pt[base:base+4]))
    for o in range(base, min(end, len(pt)), 4):
        v = struct.unpack_from('<I', pt, o)[0]
        print('   ', hex(o), hex(v), repr(pt[o:o+16]))
