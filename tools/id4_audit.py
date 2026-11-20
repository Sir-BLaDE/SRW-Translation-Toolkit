import sys, struct, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
import kpack_ln as K

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)
f4 = [f for f in c.rows if f['id'] == 4][0]
pt = c.plain(f4)
es = json.load(open(r'C:/Dev/Default Project/srwv/datos/ln_id4_es.json', encoding='utf-8'))
keys = set(es.keys())
vals = set(es.values())

def align4(v):
    return (v + 3) & ~3

def classify(t):
    if t in keys: return 'EN'
    if t in vals: return 'ES'
    return '??'

# primary
off = 0x10
n = 0
prim_en = []
while off + 0x40 <= len(pt):
    ln = struct.unpack_from('<I', pt, off + 0x3c)[0]
    if not (0 < ln <= 0x1000): break
    txt = pt[off+0x40:off+0x40+ln].split(b'\0')[0].decode('utf-8','replace')
    st = classify(txt)
    if st != 'ES' and txt:
        prim_en.append((n, hex(off), ln, st, txt))
    off += 0x48 + align4(ln)
    n += 1

print('=== PRIMARY: records', n, ' non-ES:', len(prim_en))
for r in prim_en:
    print('  ', r)

# compact: dump raw region 0x2bb0..end in 16-byte rows for manual inspection
print('\n=== COMPACT raw dump from 0x2bb0 to end (len %s) ===' % hex(len(pt)))
for i in range(0x2bb0, len(pt), 16):
    chunk = pt[i:i+16]
    printable = ''.join(chr(x) if 32 <= x < 127 else '.' for x in chunk)
    print('%s  %s  %s' % (hex(i), chunk.hex(' '), printable))
