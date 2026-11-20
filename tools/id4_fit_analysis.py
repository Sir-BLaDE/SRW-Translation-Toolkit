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
slots = {}  # english title -> slot (first occurrence)
while off + 0x40 <= len(pt):
    ln = struct.unpack_from('<I', pt, off + 0x3c)[0]
    if not (0 < ln <= 0x1000): break
    txt = pt[off+0x40:off+0x40+ln].split(b'\0')[0].decode('utf-8','replace')
    if txt in es and txt not in slots:
        slots[txt] = ln
    off += 0x48 + align4(ln)

print('English titles still present:', len(slots))
print('%-45s %5s %5s %6s  %s' % ('EN','ln','trLen','delta','ES'))
over = []
for en, ln in slots.items():
    tr = es[en]
    trlen = len(tr.encode('utf-8'))
    delta = trlen - ln
    flag = 'OK' if trlen + 1 <= ln else 'OVER' if delta > 0 else ''
    print('%-45s %5d %5d %6d  %-3s %s' % (en[:45], ln, trlen, delta, flag, tr[:60]))
    if trlen + 1 > ln:
        over.append((en, ln, trlen, tr))

print('\nOver count:', len(over))
