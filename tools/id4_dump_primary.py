import sys, struct, json
sys.path.insert(0, r'C:/Dev/Default Project/srwv/tools')
from cpk_util import load
import kpack_ln as K

P = r'D:/Juegos/-SPARROW-/Super Robot Wars V/Data/KURODATA/EN/KPACK_P4_LN_EN.CPK'
c = load(P)
f4 = [f for f in c.rows if f['id'] == 4][0]
pt = c.plain(f4)

es = json.load(open(r'C:/Dev/Default Project/srwv/datos/ln_id4_es.json', encoding='utf-8'))

def align4(v):
    return (v + 3) & ~3

off = 0x10
n = 0
recs = []
while off + 0x40 <= len(pt):
    key = pt[off:off+4]
    ln = struct.unpack_from('<I', pt, off + 0x3c)[0]
    if not (0 < ln <= 0x1000):
        break
    raw = pt[off+0x40:off+0x40+ln]
    txt = raw.split(b'\0')[0].decode('utf-8', 'replace')
    slot = align4(ln)
    tr = es.get(txt)
    state = 'ES' if tr else 'EN'
    recs.append((n, off, key.decode('ascii','replace'), ln, slot, txt, tr))
    off += 0x48 + slot
    n += 1

print('primary records', n, 'end', hex(off))
en_left = [r for r in recs if r[6] is None]
print('still English in primary:', len(en_left))
for i, off, key, ln, slot, txt, tr in en_left:
    print('%3d %-5s ln=%3d slot=%3d %r' % (i, key, ln, slot, txt))
